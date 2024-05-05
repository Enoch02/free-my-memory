import unittest
import psutil
import subprocess
from main import kill_java


# TODO: make the function pass this test
class Tests(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

        command = ["javac", "Sleeper.java"]
        subprocess.Popen(command)
        command1 = ["java", "Sleeper"]
        subprocess.Popen(command1)

        command2 = ["javac", "Loop.java"]
        subprocess.Popen(command2)
        command3 = ["java", "Loop"]
        subprocess.Popen(command3)

    def test_kill_java(self):
        kill_java(delay=0)

        processes = psutil.process_iter()
        running_java_count = 0

        for process in processes:
            if "java" in process.name():
                if process.status == "running":
                    running_java_count += 1

        print(f"count: {running_java_count}")
        self.assertTrue(running_java_count == 0)


if __name__ == "__main__":
    unittest.main()
