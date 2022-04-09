#!/usr/bin/env python3

import argparse
import pprint
import time
from orchestrator import Orchestrator, DEFAULT_CONFIG_FILE

MASTER_AUTO_UPDATE_CHECK_THRESHOLD_DEFAULT = 3
MASTER_AUTO_UPDATE_INTERVAL_SECONDS_DEFAULT = 5

pp = pprint.PrettyPrinter(indent=4)

class AutoUpdater(Orchestrator):

    def __init__(self, config_file=None, args={}):
        super().__init__(config_file, args)
        self.action_white_list= ["mysql-stop","mysql-start","set-read-only","set-writeable","mysql-install",
                                 "cluster-install","audittest"]

    # def set_instance_read_only(self, hostname, port=3306):
    #     self.logger.debug("Setting %s:%d writable" % (hostname, port))
    #     return self.instance_action('set-read-only', hostname, port)
    #
    # def set_instance_writeable(self, hostname, port=3306):
    #     self.logger.debug("Setting %s:%d writable" % (hostname, port))
    #     return self.instance_action('set-writeable', hostname, port)

    def run(self,host,port,action,parmeter):
        self.logger.info("Starting %s, on %s %s" % (action,host,port))
        try:
            if action not in self.action_white_list:
                self.logger.error("unkown action %s" % (action))
                return
            if action == "cluster-install":
                 # parmeter format clustername:xxxx,master:xxxxx,slave:[xxxx,xxxx],
                pass
            if action == "createdb":
                 # parmeter format owner:xxx,product:xxxx
                pass
            data = self.instance_action(action,parmeter, host, port)
            pp.pprint(data)
        except KeyboardInterrupt:
            self.logger.warning('Process interrupted')
        except Exception as e:
            self.logger.error(e)
def main():
    parser = argparse.ArgumentParser(description="Manage nftables sets")
    parser.add_argument("--debug", action='store_true', help="Enable debugging")
    parser.add_argument("--quiet", action='store_true', help="Silence output except for errors")
    parser.add_argument("--config-file", type=str, metavar="FILE", default=DEFAULT_CONFIG_FILE, help="Configuration filepath, default: %s" % DEFAULT_CONFIG_FILE)
    parser.add_argument("-i", "--ip", type=str, metavar="ALIAS", help="agent host")
    parser.add_argument("-P", "--port", type=str, metavar="ALIAS", help="agent mysql port")
    parser.add_argument("-a", "--action", type=str, metavar="ALIAS", help="action on mysql agent")
    parser.add_argument("-p", "--parmeter", type=str, metavar="ALIAS",help="action parameter")
    args = vars(parser.parse_args())
    config_file = args.pop('config_file')
    host = args.pop('ip')
    port = args.pop('port')
    action = args.pop('action')
    parmeter = args.pop('parmeter')

    auto_updater = AutoUpdater(config_file, args)
    auto_updater.run(host,port,action,parmeter)


if __name__ == "__main__":
    main()
