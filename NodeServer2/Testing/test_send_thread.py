import threading
import time
from abc import ABC, abstractmethod

class PrintStrategy(ABC):
    @abstractmethod
    def should_print(self, mailbox):
        pass

class TimedPrintStrategy(PrintStrategy):
    def __init__(self, interval):
        self.interval = interval
        self.last_print_time = time.time()

    def should_print(self, mailbox):
        current_time = time.time()
        if current_time - self.last_print_time >= self.interval:
            self.last_print_time = current_time
            return True
        return False

class ThresholdStrategy(PrintStrategy):
    def __init__(self, threshold):
        self.threshold = threshold

    def should_print(self, mailbox):
        return len(mailbox.mails) >= self.threshold

class Mailbox:
    def __init__(self, strategy):
        self.mails = []
        self.lock = threading.Lock()
        self.strategy = strategy
        self.print_thread = threading.Thread(target=self.process_mails)
        self.print_thread.start()

    def add_mail(self, mail):
        with self.lock:
            self.mails.append(mail)
            print("Added mail", mail)

    def process_mails(self):
        while True:
            with self.lock:
                if self.strategy.should_print(self):
                    print("Printing mails:")
                    print("\n".join(self.mails))
                    self.mails.clear()
            time.sleep(1)  # Small sleep to prevent this loop from consuming too much CPU

    def stop(self):
        self.print_thread.join()

# Example usage
timed_strategy = TimedPrintStrategy(interval=30)
threshold_strategy = ThresholdStrategy(threshold=30)
mailbox = Mailbox(strategy=threshold_strategy)

for i in range(35):
    mailbox.add_mail(f"Mail {i + 1}")
    time.sleep(1)

mailbox.stop()
