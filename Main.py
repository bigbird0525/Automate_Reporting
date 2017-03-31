import queue
import threading
import Automated_Reporting
import Access_DB
lock = threading.Lock()
cred_queue = queue.Queue()

class RunDrivers(threading.Thread):

    def __init__(self):
        super().__init__()

    def __call__(self):
        global cred_queue

        while True:
            try:
                lock.acquire()
                cred = cred_queue.get(timeout=1)
                lock.release()
                if not cred:
                    break

                if cred['Platform'] == 'LKQD':
                    Automated_Reporting.LKQD(cred).exe()

                elif cred['Platform'] == 'Streamrail':
                    Automated_Reporting.Streamrail(cred).exe()

                elif cred['Platform'] == 'Verta':
                    Automated_Reporting.Verta(cred).exe()

                elif cred['Platform'] == 'Optimatic':
                    pass

                elif cred['Platform'] == 'Springserve':
                    pass
            except queue.Empty:
                break

class Threader(Runnable):

    def __init__(self):
        super().__init__()

    def load(self, credentials):
        global cred_queue
        threads = []

        for row in credentials:
            cred_queue.put(row)

        for i in range(4):
            new_thread = threading.Thread(target=RunDrivers())
            threads.append(new_thread)
            new_thread.daemon = True
            new_thread.start()

        for thread in threads:
            thread.join()

if __name__ == "__main__":
    logins = Automated_Reporting.GetCredentials().run("logins.csv")
    Access_DB.Access_DB('external_partners.db').create_db()
    Threader().load(logins)
