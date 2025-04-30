import json
import subprocess

def load_config():
    with open('config.json') as f:
        return json.load(f)

def run_mutation_tests():
    subprocess.run([
        'mut.py',
        '--target', 'Services.main',
        '--unit-test', 'Test.appointments_test',
        '--runner', 'unittest'
    ], check=True)

def run_normal_tests():
    subprocess.run(['python', '-m', 'unittest', 'Test.appointments_test'], check=True)

def main():
    config = load_config()
    if config.get("mutation", False):
        print("[*] Running mutation tests...")
        run_mutation_tests()
    else:
        print("[*] Running normal tests...")
        run_normal_tests()

from test_runner import main
if __name__ == "__main__":
    main()
