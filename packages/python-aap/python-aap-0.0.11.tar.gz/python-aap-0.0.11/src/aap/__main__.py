import os
import time
import argparse
import json
import urllib3

from . import JobTemplate, API


def main():
    parser = argparse.ArgumentParser(
        description="Trigger jobs and workflows from terminal",
    )
    # More will be added later
    parser.add_argument("action", choices=["run-job"])
    parser.add_argument('-i', '--id', dest="id", action="store",
                        required=True, help="ID of job to run")
    parser.add_argument('-f', '--follow', action="store_true", default=False,
                        help="Wait for job to finish execution and report its status")
    parser.add_argument('-p', '--password', dest="password", action="store", default=os.environ.get(
        "AAP_PASSWORD"), help="Password used for authentication to AAP API (env: AAP_PASSWORD)")
    parser.add_argument('-u', '--username', dest="username", action="store", default=os.environ.get(
        "AAP_USERNAME"), help="Username used for authentication to AAP API (env: AAP_USERNAME)")
    parser.add_argument('-s', '--url', dest="url", action="store",
                        default=os.environ.get('AAP_URL'), help="URL of AAP instance (env: AAP_URL)")
    parser.add_argument('--insecure', dest="insecure", action="store_true",
                        default=False, help="Dont verify ssl certificate")
    parser.add_argument('-l', '--limit', dest="limit", action="store",
                        default=[], help="Limit as comma separated list")
    parser.add_argument('-j', '--tags', dest="tags", action="store",
                        default=[], help="Job tags as comma separated list")
    parser.add_argument('-e', '--extra-vars', dest="extra", action="store",
                        default={}, help="json formatted extra variables")
    parser.add_argument('-r', '--retries', dest="retries", action="store",
                        type=int, default=3, help="Number of retries on API error")
    parser.add_argument('-t', '--poll-timeout', dest="timeout", action="store",
                        type=int, default=5, help="Number of seconds between 2 polling requests to aap")
    parser.add_argument('--ignore-fail', dest="ingore_fail", action="store_true",
                        default=False, help="Program will return successfull even if job fails")

    args = parser.parse_args()

    if not args.username or not args.password or not args.url:
        print("Please provide AAP URL and credentials,"
              "either using command line arguments or by setting environment variables.")
        parser.print_help()
        exit(1)

    if args.limit:
        args.limit = args.limit.split(',')
    if args.tags:
        args.tags = args.tags.split(',')
    if args.extra:
        try:
            args.extra = json.loads(args.extra)
        except ValueError:
            print(f"Invalid extra variables provided: {args.extra}")
            exit(1)
    if args.insecure:
        urllib3.disable_warnings()

    aap = API(args.url, args.username, args.password,
              ssl_verify=not args.insecure, retries=args.retries)
    print(f"Searching job {args.id}")
    template = JobTemplate.load(args.id, aap)
    if not template:
        print("Job not found")
        exit(1)
    print(f"Job: {template.name}")
    print(f"\tlimit: {args.limit}")
    print(f"\textra variables: {args.extra}")
    print(f"\tjob tags: {args.tags}")
    job = template.launch(args.extra, args.limit, args.tags)
    print(f"\tjob url: {job.url}")

    if not args.follow:
        exit(0)

    print('-' * 40)
    state = job.status
    print(f"Job is {state}")

    while not job.is_running and not job.is_finished:
        time.sleep(args.timeout)
        job._reload()
        if job.status != state:
            state = job.status
            print(f"Job is {state}")
    try:
        last_line = 0
        while job.is_running:
            stdout = job.stdout.splitlines()
            if len(stdout) > last_line:
                print("\n".join(stdout[last_line:]))
                last_line = len(stdout)
            time.sleep(args.timeout)
            job._reload()

        stdout = job.stdout.splitlines()
        if len(stdout) > last_line:
            print("\n".join(stdout[last_line:]))
            last_line = len(stdout)
    except Exception:
        print("Error happend during fetching of output")
        state = job.status
        print(f"Job is {state}")
        while job.is_running:
            time.sleep(args.timeout)
            job._reload()
            if job.status != state:
                state = job.status
                print(f"Job is {state}")

    exit(not (job.is_successfull or args.ingore_fail))


if __name__ == "__main__":
    main()
