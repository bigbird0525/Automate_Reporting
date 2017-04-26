import queue
import threading
import Automated_Reporting
import DB
lock = threading.Lock()
cred_queue = queue.Queue()


class Runnable(threading.Thread):

    def __init__(self):
        super().__init__()


    def __call__(self):
        global cred_queue

        try:
            while not cred_queue.empty():
                lock.acquire()
                cred = cred_queue.get()
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
                    # Automated_Reporting.Springserve(cred).exe()
                    pass
        finally:
            cred_queue.task_done()
        # lock.acquire()
        # cred = cred_queue.get()
        # lock.release()
        # if not cred:
        #     pass
        # if cred['Platform'] == 'LKQD':
        #     Automated_Reporting.LKQD(cred).exe()
        #
        # elif cred['Platform'] == 'Streamrail':
        #     Automated_Reporting.Streamrail(cred).exe()
        #
        # elif cred['Platform'] == 'Verta':
        #     Automated_Reporting.Verta(cred).exe()
        #
        # elif cred['Platform'] == 'Optimatic':
        #     pass
        #
        # elif cred['Platform'] == 'Springserve':
        #     # Automated_Reporting.Springserve(cred).exe()
        #     pas

class Threader(Runnable):
    def __init__(self):
        super().__init__()

    def load(self, credentials):
        global cred_queue
        threads = []

        for row in credentials:
            cred_queue.put(row)

        for i in range(4):
            threads.append(threading.Thread(target=Runnable()))
            threads[-1].daemon = True
            threads[-1].start()

        for thread in threads:
            thread.join()

        print("Closing threads")

if __name__ == "__main__":
    logins = Automated_Reporting.GetCredentials().run('logins.csv')
    DB.Access_DB('external_partners.db').create_db()
    Threader().load(logins)
