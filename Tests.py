import hashlib
import os
import random

"""
This file contains test cases for the Forwarder. You can add test cases here,
and then use them in the forwarder.
"""

class BTPTest(object):
    """ A test case should define the following:
        - handle_packet: a method to be called whenever a packet arrives
        - handle_tick: a method to be called at every timestemp
        - result: a method to be called when it's time to return a result
    """
    def __init__(self, forwarder, input_file):
        self.forwarder = forwarder

        if not os.path.exists(input_file):
            raise ValueError("Could not find input file: %s" % input_file)
        self.input_file = input_file
        self.forwarder.register_test(self, self.input_file)

    def handle_packet(self):
        """
        This method is called whenever the forwarder receives a packet,
        immediately after the packet has been added to the forwarder's input
        queue.

        The default behavior of the base class is to simply copy whatever is in
        the input queue to the output queue, in the order it was received.
        Most tests will want to override this, since this doesn't give you the
        opportunity to do anything tricksy with the packets.

        Note that you should NEVER make any assumptions about how many packets
        are in the in_queue when this method is called -- there could be zero,
        one, or many!
        """
        for p in self.forwarder.in_queue:
            self.forwarder.out_queue.append(p)
        # empty out the in_queue
        self.forwarder.in_queue = []

    def handle_tick(self, tick_interval):
        """
        This method is called whenever the forwarder has a tick event. This
        gives the test case an opportunity to create behavior that is not
        triggered by packet arrivals. The forwarder will provide the tick
        interval to the test case.

        The default behavior of this method is to do nothing.
        """
        pass

    def result(self, receiver_outfile):
        """
        This should return some meaningful result. You could do something
        like check to make sure both the input and output files are identical,
        or that some other aspect of your test passed. This is called
        automatically once the forwarder has finished executing the test.

        You can return whatever you like, or even just print a message saying
        the test passed. Alternatively, you could use the return value to
        automate testing (i.e., return "True" for every test that passes,
        "False" for every test that fails).
        """
        if self.files_are_the_same(self.input_file, receiver_outfile):
            print "Test passes!"
            return True
        else:
            print "Test fails: original file doesn't match received. :("
            return False

    # Utility methods -- not necessary, just helpful for writing tests
    def files_are_the_same(self, file1, file2):
        """
        Checks if the contents of two files are the same. Returns True if they
        are, and False otherwise.
        """
        return BTPTest.md5sum(file1) == BTPTest.md5sum(file2)

    @staticmethod
    def md5sum(filename, block_size=2**20):
        """
        Calculates the md5sum of a file.
        """
        f = open(filename, "rb")
        md5 = hashlib.md5()
        while True:
            data = f.read(block_size)
            if not data:
                break
            md5.update(data)
        f.close()
        return md5.digest()

"""
This tests random packet drops. We randomly decide to drop about half of the
packets that go through the forwarder in either direction.

Note that to implement this we just needed to override the handle_packet()
method -- this gives you an example of how to extend the basic test case to
create your own.
"""
class RandomDropTest(BTPTest):
    def handle_packet(self):
        for p in self.forwarder.in_queue:
            if random.choice([True, False]):
                self.forwarder.out_queue.append(p)

        # empty out the in_queue
        self.forwarder.in_queue = []
