/*
* @Author: djvolz
* @Date:   2016-11-14 00:26:18
* @Last Modified by:   djvolz
* @Last Modified time: 2016-11-15 00:33:16
*/
/**
 * This skill triggers a message queue that instructs a raspberry pi to invoke
 * commands.
 */

var AWS = require('aws-sdk');
var sequences = require('./sequences');

var sqs = new AWS.SQS({region : 'us-east-1'});

var AWS_ACCOUNT = '';
var QUEUE_NAME  = '';
var QUEUE_URL   = '';

// Route the incoming request based on type (LaunchRequest, IntentRequest,
// etc.) The JSON body of the request is provided in the event parameter.
exports.handler = function (event, context) {
    try {
        console.log("event.session.application.applicationId=" + event.session.application.applicationId);

        /**
         * This validates that the applicationId matches what is provided by Amazon.
         */
        if (event.session.application.applicationId !== "amzn1.ask.skill.d023ff43-73d6-4ecb-91be-34182bcb1ec8") {
             context.fail("Invalid Application ID");
        }

        if (event.session.new) {
            onSessionStarted({requestId: event.request.requestId}, event.session);
        }

        if (event.request.type === "LaunchRequest") {
            onLaunch(event.request,
                event.session,
                function callback(sessionAttributes, speechletResponse) {
                    context.succeed(buildResponse(sessionAttributes, speechletResponse));
                });
        } else if (event.request.type === "IntentRequest") {
            onIntent(event.request,
                event.session,
                function callback(sessionAttributes, speechletResponse) {
                    context.succeed(buildResponse(sessionAttributes, speechletResponse));
                });
        } else if (event.request.type === "SessionEndedRequest") {
            onSessionEnded(event.request, event.session);
            context.succeed();
        }
    } catch (e) {
        context.fail("Exception: " + e);
    }
};

/**
 * Called when the session starts.
 */
function onSessionStarted(sessionStartedRequest, session) {
    console.log("onSessionStarted requestId=" + sessionStartedRequest.requestId +
        ", sessionId=" + session.sessionId);
}

/**
 * Called when the user launches the skill without specifying what they want.
 */
function onLaunch(launchRequest, session, callback) {
    console.log("onLaunch requestId=" + launchRequest.requestId +
        ", sessionId=" + session.sessionId);

    // Dispatch to your skill's launch.
    getWelcomeResponse(callback);
}

/**
 * Called when the user specifies an intent for this skill. This drives
 * the main logic for the function.
 */
function onIntent(intentRequest, session, callback) {
    console.log("onIntent requestId=" + intentRequest.requestId +
        ", sessionId=" + session.sessionId);

    var intent = intentRequest.intent,
        intentName = intentRequest.intent.name;

    // Dispatch to the individual skill handlers

    if ("SequenceIntent" === intentName) {
        sequenceIntent(intent, session, callback);
    }  else if ("AMAZON.StartOverIntent" === intentName) {
        getWelcomeResponse(callback);
    } else if ("AMAZON.HelpIntent" === intentName) {
        getHelpResponse(session, callback);
    } else if ("AMAZON.RepeatIntent" === intentName) {
        getWelcomeResponse(callback);
    } else if ("AMAZON.StopIntent" === intentName || "AMAZON.CancelIntent" === intentName) {
        handleSessionEndRequest(callback);
    } else {
        throw "Invalid intent";
    }
}

/**
 * Called when the user ends the session.
 * Is not called when the skill returns shouldEndSession=true.
 */
function onSessionEnded(sessionEndedRequest, session) {
    console.log("onSessionEnded requestId=" + sessionEndedRequest.requestId +
        ", sessionId=" + session.sessionId);
}

// --------------- Base Functions that are invoked based on standard utterances -----------------------

// this is the function that gets called to format the response to the user when they first boot the app

function getWelcomeResponse(callback) {
    var sessionAttributes = {};
    var shouldEndSession = false;
    var cardTitle = "Welcome to Robot Roxie";

    var speechOutput = "Hello. I've been watching you.";

    var cardOutput = "It's true.";

    var repromptText = "Either way, what do you want me to do with the lights?";

    console.log('speech output : ' + speechOutput);

    callback(sessionAttributes,
        buildSpeechletResponse(cardTitle, speechOutput, cardOutput, repromptText, shouldEndSession));
}

// this is the function that gets called to format the response to the user when they ask for help
function getHelpResponse(session, callback) {
    var sessionAttributes = {};
    var cardTitle = "Carl Lights Help";
    // this will be what the user hears after asking for help

    // first check if a session exists, if so save so it won't be lost
    if (session.attributes) {
        sessionAttributes = session.attributes;
    }

    var speechOutput = "However beautiful the strategy, you should occasionally look at the results.";

    // if the user still does not respond, they will be prompted with this additional information
    
    var repromptText = "Taste is chocolate, smooth, not bitter, a bit sweet. Mouthfeel is short of chewy. I found a new one for my favorites list.";

    var shouldEndSession = true;

    callback(sessionAttributes,
        buildSpeechletResponse(cardTitle, speechOutput, speechOutput, repromptText, shouldEndSession));
}

// this is the function that gets called to format the response when the user is done
function handleSessionEndRequest(callback) {
    var cardTitle = "Get outta here.";
    
    var speechOutput = "Hey whatchu doing later.";

    // Setting this to true ends the session and exits the skill.

    var shouldEndSession = true;

    callback({}, buildSpeechletResponse(cardTitle, speechOutput, speechOutput, null, shouldEndSession));
}


// Control lights
function sequenceIntent(intent, session, callback) {
    var repromptText = "What else can I help with?";
    var shouldEndSession = true;
    var speechOutput;
    var sessionAttributes = {};

    if (session.attributes) {
        sessionAttributes = session.attributes;
    } 
    
    var sequenceName = null;
    var sequenceSlot = intent.slots.Sequence;
    if (sequenceSlot && sequenceSlot.value){
        sequenceName = sequenceSlot.value.toLowerCase();
    } 

    if (sequenceName in sequences) {
        var cardTitle = "Putting on " + sequenceName;
        speechOutput = "Get ready, here comes " + sequenceName;

        console.log("Sending Message to SQS Queue");

        var lightsRequest = {};
            lightsRequest.action = sequenceName;

        // package data to be sent
        var sendData = {};
            sendData.request = lightsRequest;

        // set parameters for message queue to transport data        
        var params = {
            MessageBody: JSON.stringify(sendData),
            QueueUrl: QUEUE_URL + AWS_ACCOUNT + '/' + QUEUE_NAME
        };

        // send message to SQS and return back message to Alexa
        sqs.sendMessage(params, function(err, data){
            if(err) {
                console.log('error:',"Fail Send Message" + err);
                callback(sessionAttributes,
                    buildSpeechletResponse(err, "Error", "Error", "Error", true));
            } else {
                console.log('successful post - data:',data.MessageId);
                callback(sessionAttributes,
                buildSpeechletResponse(cardTitle, speechOutput, speechOutput, repromptText, shouldEndSession));
            }
        });
    } else {
        if (sequenceName) {
            speechOutput = "I'm sorry, I currently do not know how to do " + sequenceName + ". What else can I help with?";
        } else {
            speechOutput = "I'm sorry, I currently do not know that sequence. What else can I help with?";
        }

        shouldEndSession = false;

        callback(sessionAttributes,
            buildSpeechletResponse("Not found", speechOutput, speechOutput, repromptText, shouldEndSession));
    }
}


// --------------- Helpers that build all of the responses -----------------------

function buildSpeechletResponse(title, output, cardInfo, repromptText, shouldEndSession) {
    return {
        outputSpeech: {
            type: "PlainText",
            text: output
        },
        card: {
            type: "Simple",
            title: title,
            content: cardInfo
        },
        reprompt: {
            outputSpeech: {
                type: "PlainText",
                text: repromptText
            }
        },
        shouldEndSession: shouldEndSession
    };
}

function buildResponse(sessionAttributes, speechletResponse) {
    return {
        version: "1.0",
        sessionAttributes: sessionAttributes,
        response: speechletResponse
    };
}

