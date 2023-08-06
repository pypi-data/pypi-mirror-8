
// This was originally a Python test from Marian Aioanei.  She and I got it down to something mostly minimal.
// From there I've ported it to Java, and found that it demonstrates that the original Java code does not
// have the same problem.
import java.util.*;

class TestFibonacciHeap {
    public static void main(final String[] arguments) {
        FibonacciHeap<Integer> min_prio_queue = new FibonacciHeap<>();
        Integer expected_count = 17;
        ArrayList<FibonacciHeap.Entry<Integer>> map_entries = new ArrayList<FibonacciHeap.Entry<Integer>>();
        for (int index=0; index < expected_count; index++) {
            FibonacciHeap.Entry<Integer> entry = min_prio_queue.enqueue(index, 2.0);
            map_entries.add(entry);
        }

        FibonacciHeap.Entry<Integer> entry = min_prio_queue.dequeueMin();
        expected_count -= 1;

        for (int index=10; index > 7; index--) {
            min_prio_queue.decreaseKey(map_entries.get(index), 1.0);
        }

        int actual_count = 0;
        while (!min_prio_queue.isEmpty()) {
            entry = min_prio_queue.dequeueMin();
            actual_count += 1;
        }

        if (actual_count != expected_count) {
            System.out.println("test failed; actual_count: " + actual_count + ", expected_count: " + expected_count);
        } else {
            System.out.println("test passed");
        }

    }
}
