#!/usr/bin/env python

"""
Copyright llamy contributors.

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.
"""

from argparse import ArgumentParser
from llamy.get_banner import get_banner
from pkg_resources import get_distribution

llamy_version = get_distribution('llamy').version


def main():
    """
    Application's entry point.

    Here, application's settings are read from the command line,
    environment variables and CRD. Then, retrieving and processing
    of Kubernetes events are initiated.
    """
    parser = ArgumentParser(
        description='llamy - CLI',
        prog='llamy'
    )

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s ' + llamy_version
    )

    parser.add_argument(
        '-b',
        '--banner',
        action='store_true',
        help="Print llamy's banner"
    )

    args = parser.parse_args()

    # print("llamy called with the folowing parameters")
    # print(parser.parse_args())

    if args.banner:
        print(get_banner())
        exit()
