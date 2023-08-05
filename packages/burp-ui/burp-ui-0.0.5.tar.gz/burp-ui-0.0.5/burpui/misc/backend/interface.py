# -*- coding: utf8 -*-

class BUIbackend:
    def __init__(self, app=None, host='127.0.0.1', port=4972):
        self.app = app
        self.host = host
        self.port = port

    def status(self, query='\n', agent=None):
        raise NotImplementedError("Sorry, the current Backend does not implement this method!")

    def parse_backup_log(self, f, n, c=None, agent=None):
        raise NotImplementedError("Sorry, the current Backend does not implement this method!")

    def get_counters(self, name=None, agent=None):
        raise NotImplementedError("Sorry, the current Backend does not implement this method!")

    def is_backup_running(self, name=None, agent=None):
        raise NotImplementedError("Sorry, the current Backend does not implement this method!")

    def is_one_backup_running(self, agent=None):
        raise NotImplementedError("Sorry, the current Backend does not implement this method!")

    def get_all_clients(self, agent=None):
        raise NotImplementedError("Sorry, the current Backend does not implement this method!")

    def get_client(self, name=None, agent=None):
        raise NotImplementedError("Sorry, the current Backend does not implement this method!")

    def get_tree(self, name=None, backup=None, root=None, agent=None):
        raise NotImplementedError("Sorry, the current Backend does not implement this method!")

class BUIserverException(Exception):
    pass
