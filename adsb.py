import socket
import time
import logging
import argparse
from datadog import statsd
import sbs1
logging.basicConfig(level=logging.INFO)


def fetch_data(skt):
    msg = skt.recv(1024)
    if len(msg) < 20:
        raise Exception("Socket contained malformed data")
    return msg


def parse_data(msg):
    return sbs1.SBS1Message(msg.decode('utf-8'))


def log_dawg(sbs):
    statsd.increment("adsb.message", '1')
    if sbs.groundSpeed is not None: statsd.gauge('adsb.airspeed', sbs.groundSpeed)
    if sbs.altitude is not None: statsd.gauge('adsb.altitude', sbs.altitude)
    if sbs.track is not None: statsd.histogram('adsb.heading', sbs.track)
    if sbs.verticalRate is not None:
        if sbs.verticalRate > 0:
            statsd.gauge('adsb.ascentrate', sbs.verticalRate)
        else:
            statsd.gauge('adsb.decentrate', sbs.verticalRate)



def fetch_loop(skt):
    while True:
        msg = fetch_data(skt)
        sbs_message = parse_data(msg)
        logging.info(sbs_message.toJSON())
        log_dawg(sbs_message)


def start_socket(args):
    logging.info("Connecting to {} {}...".format(args.host, args.port))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((args.host, args.port))
    logging.info("Connected to {}:{}".format(args.host, args.port))
    return s


def main_loop(args):
    while True:
        try:
            skt = start_socket(args)
            fetch_loop(skt)
        except Exception as error:
            logging.error(error)
        finally:
            try:
                skt.close()
            except Exception as close_error:
                logging.error("Could not close broken socket")
                logging.error(close_error)
        logging.error("Shit went bad. Attempting to restart connection")
        time.sleep(5)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="Hostname of the ADSB server. Default: localhost", default="localhost")
    parser.add_argument("--port", help="Port of the ADSB server. Default is 30003", type=int, default=30003)

    main_loop(parser.parse_args())