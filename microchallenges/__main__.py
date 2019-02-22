import argparse
import logging
from framework.framework import main

if __name__ == "__main__":
    level = logging.INFO
    logging.basicConfig(format="%(asctime)s -- %(levelname)s: %(message)s",
                        level=level)
    logging.info("======================== CHALLENGE SERVER SIDE LOGS ========================")
    parser = argparse.ArgumentParser(
        usage="%(prog)s [options] CHALLENGE_NAME SERVICE_URL\n       %(prog)s [options] -r FILE")
    parser.add_argument("challenge_name", nargs="?", default="challenge_name",
                        metavar="CHALLENGE_NAME")
    parser.add_argument("service_url", nargs="?", default="http://localhost:3000",
                        metavar="SERVICE_URL")
    parser.add_argument("-w", nargs="?", default="replayfile",
                        metavar="REPLAY_FILE")
    parser.add_argument("-o", nargs="?", default="results.json",
                        metavar="RESULTS_JSON_FILE")
    parser.add_argument("-n", nargs="?", default="chuck-norris",
                        metavar="TEAM_NAME")
    parser.add_argument("--max_timeout", nargs="?", default=20,
                        metavar="MAX_TIMEOUT")
    parser.add_argument("--connect_timeout", nargs="?", default=20,
                        metavar="CONNECT_TIMEOUT")
    parser.add_argument("--duration", nargs="?", default=15,
                        metavar="DURATION")
    args = parser.parse_args()

    score = main(
        args.challenge_name,
        args.w,
        args.o,
        args.service_url,
        args.n,
        args.max_timeout,
        args.connect_timeout,
        args.duration)

    logging.info("Total score: %s points", str(score))
    logging.info("===================== END OF CHALLENGE SERVER LOGS =====================")
