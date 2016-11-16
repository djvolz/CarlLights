# -*- coding: utf-8 -*-
# @Author: djvolz
# @Date:   2016-11-14 17:46:12
# @Last Modified by:   djvolz
# @Last Modified time: 2016-11-15 19:32:34

import os
from control import Controller


def main():
    controller = Controller()

    try:
        # DO PROGRAM THAT WE WROTE, MAKE VALHALLA PRETTY
        controller.run()

    # these aren't caught with exceptions...
    except (KeyboardInterrupt, SystemExit):
        print("except (KeyboardInterrupt, SystemExit):")
        os._exit(0)
    except Exception as e:
        print("EXCEPTION:")
        print(e)
        # kill process immediately so it can be respawned by the service.
        os._exit(0)


if __name__ == '__main__':
    main()
