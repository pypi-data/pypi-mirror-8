#!/usr/bin/python

import os
import sys
import commands
import requests
import argparse
from json import dumps
from urllib import urlencode
from xml.dom.minidom import parseString

version = VERSION = __version__ = '0.3.0'


def generate_report(path):
    try:
        with open(path, 'r') as f:
            return generate_json(f.read())
    except:
        try:
            commands.getstatusoutput('coverage xml')
        except:
            return None
        else:
            try:
                with open(path, 'r') as f:
                    return generate_json(f.read())
            except:
                raise AssertionError("no coverage.xml file could be found or generated")

def generate_json(xml):
    coverage = parseString(xml).getElementsByTagName('coverage')[0]
    if coverage.getAttribute('generated'):
        # clover xml
        return dict(meta=dict(package="coverage/clover", version="codecov-python/v%s"%VERSION),
                    coverage=dict(map(_clover_coverage, coverage.getElementsByTagName('file'))))
    else:
        # standard python coverage
        for package in coverage.getElementsByTagName('package'):
            if package.getAttribute('name') == '':
                return dict(meta=dict(package="coverage/v%s"%coverage.getAttribute('version'), version="codecov-python/v%s"%VERSION),
                            stats=dict(branches=dict(map(_branches, coverage.getElementsByTagName('class')))),
                            coverage=dict(map(_coverage, coverage.getElementsByTagName('class'))))

def _clover_coverage(_class):
    """ex.
    <file name="/Users/peak/Documents/codecov/codecov-php/src/Codecov/Coverage.php">
      <class name="Coverage" namespace="Codecov">
        <metrics methods="1" coveredmethods="0" conditionals="0" coveredconditionals="0" statements="4" coveredstatements="1" elements="5" coveredelements="1"/>
      </class>
      <line num="5" type="method" name="send" crap="154.69" count="1"/>
      <line num="8" type="stmt" count="1"/>
      <line num="18" type="stmt" count="0"/>
      <line num="19" type="stmt" count="0"/>
      <line num="20" type="stmt" count="0"/>
      <metrics loc="83" ncloc="59" classes="1" methods="1" coveredmethods="0" conditionals="0" coveredconditionals="0" statements="4" coveredstatements="1" elements="5" coveredelements="1"/>
    </file>
    """
    _lines = _class.getElementsByTagName('line')
    if not _lines:
        return _class.getAttribute('file'), []

    lines = [None]*(max([int(line.getAttribute('num')) for line in  _lines])+1)
    for line in _lines:
        lines[int(line.getAttribute('num'))] = int(line.getAttribute('count') or 0)

    return _class.getAttribute('name'), lines

def _coverage(_class):
    """
    Lines Covered
    =============

    <class branch-rate="0" complexity="0" filename="file.py" line-rate="1" name="module">
        <methods/>
        <lines>
            <line hits="1" number="1"/>
            <line branch="true" condition-coverage="100% (2/2)" hits="1" number="2"/>
            <line branch="true" condition-coverage="500% (1/2)" hits="1" number="3"/>
            <line hits="0" number="4"/>
        </lines>
    </class>

    {
        "file.py": [None, 1, True, 0]
    }
    """
    # available: branch
    _lines = _class.getElementsByTagName('line')
    if not _lines:
        return _class.getAttribute('filename'), []

    lines = [None]*(max([int(line.getAttribute('number')) for line in  _lines])+1)
    for line in _lines:
        cc = str(line.getAttribute('condition-coverage'))
        lines[int(line.getAttribute('number'))] = True if cc and '100%' not in cc else int(line.getAttribute('hits') or 0)

    return _class.getAttribute('filename'), lines

def _branches(_class):
    """
    How many branches found
    =======================

    <class branch-rate="0" complexity="0" filename="file.py" line-rate="1" name="module">
        <methods/>
        <lines>
            <line hits="1" number="1"/>
            <line branch="true" condition-coverage="100% (2/2)" hits="1" number="2"/>
            <line branch="true" condition-coverage="500% (1/2)" hits="1" number="3"/>
            <line hits="0" number="4"/>
        </lines>
    </class>

    {
        "file.py": 2
    }
    """
    return _class.getAttribute('filename'), sum(map(lambda l: int(l.getAttribute('condition-coverage').split('/')[1][:-1]), 
                                                    filter(lambda l: l.getAttribute('branch')=='true', 
                                                           _class.getElementsByTagName('line'))))

def upload(xml, url, **kwargs):
    try:
        args = dict(commit='', branch='', travis_job_id='')
        args.update(kwargs)
        assert args.get('branch') not in ('', None), "branch is required"
        assert args.get('commit') not in ('', None), "commit hash is required"
        assert (args.get('travis_job_id') or args.get('token')) not in (None, ''), "travis_job_id or token are required"

        coverage = generate_report(xml)
        assert coverage, "error no coverage.xml report found, could not upload to codecov"
        
        url = "%s/upload/v1?%s" % (url, urlencode(dict([(k, v) for k, v in kwargs.items() if v is not None])))
        result = requests.post(url, headers={"Content-Type": "application/json"}, data=dumps(coverage))
        return result.json()

    except AssertionError as e:
        return dict(message=str(e), uploaded=False)

def main(*argv):
    defaults = dict(commit='', branch='', travis_job_id='', xml="coverage.xml", pull_request='')

    # ---------
    # Travis CI
    # ---------
    if os.getenv('CI') == "true" and os.getenv('TRAVIS') == "true":
        # http://docs.travis-ci.com/user/ci-environment/#Environment-variables
        defaults.update(dict(branch=os.getenv('TRAVIS_BRANCH'),
                             pull_request=os.getenv('TRAVIS_PULL_REQUEST') if os.getenv('TRAVIS_PULL_REQUEST')!='false' else '',
                             travis_job_id=os.getenv('TRAVIS_JOB_ID'),
                             xml=os.path.join(os.getenv('TRAVIS_BUILD_DIR'), "coverage.xml"),
                             commit=os.getenv('TRAVIS_COMMIT')))

    # --------
    # Codeship
    # --------
    elif os.getenv('CI') == "true" and os.getenv('CI_NAME') == 'codeship':
        # https://www.codeship.io/documentation/continuous-integration/set-environment-variables/
        defaults.update(dict(branch=os.getenv('CI_BRANCH'),
                             commit=os.getenv('CI_COMMIT_ID')))

    # ---------
    # Circle CI
    # ---------
    elif os.getenv('CI') == "true" and os.getenv('CIRCLECI') == 'true':
        # https://circleci.com/docs/environment-variables
        defaults.update(dict(branch=os.getenv('CIRCLE_BRANCH'),
                             xml=os.path.join(os.getenv('CIRCLE_ARTIFACTS'), "coverage.xml"),
                             commit=os.getenv('CIRCLE_SHA1')))

    # ---------
    # Semaphore
    # ---------
    elif os.getenv('CI') == "true" and os.getenv('SEMAPHORE') == "true":
        # https://semaphoreapp.com/docs/available-environment-variables.html
        defaults.update(dict(branch=os.getenv('BRANCH_NAME'),
                             xml=os.path.join(os.getenv('SEMAPHORE_PROJECT_DIR'), "coverage.xml"),
                             commit=os.getenv('SEMAPHORE_PROJECT_HASH_ID')))
    # --------
    # drone.io
    # --------
    elif os.getenv('CI') == "true" and os.getenv('DRONE') == "true":
        # https://semaphoreapp.com/docs/available-environment-variables.html
        defaults.update(dict(branch=os.getenv('DRONE_BRANCH'),
                             xml=os.path.join(os.getenv('DRONE_BUILD_DIR'), "coverage.xml"),
                             commit=os.getenv('DRONE_COMMIT')))

    # ---
    # git
    # ---
    else:
        # find branch, commit, repo from git command
        branch = commands.getstatusoutput('git rev-parse --abbrev-ref HEAD')[1]
        defaults.update(dict(branch=branch if branch != 'HEAD' else 'master',
                             commit=commands.getstatusoutput('git rev-parse HEAD')[1]))

    parser = argparse.ArgumentParser(prog='codecov', add_help=True,
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog="""Read more at https://codecov.io/""")
    parser.add_argument('--version', action='version', version='codecov '+version+" - https://codecov.io")
    parser.add_argument('--commit', default=defaults.pop('commit'), help="commit ref")
    parser.add_argument('--branch', default=defaults.pop('branch'), help="commit branch name")
    parser.add_argument('--token', '-t', default=os.getenv("CODECOV_TOKEN"), help="codecov repository token")
    parser.add_argument('--xml', '-x', default=defaults.pop("xml"), help="coverage xml report relative path")
    parser.add_argument('--url', default="https://codecov.io", help="url, used for debugging")
    if argv:
        codecov = parser.parse_args(argv)
    else:
        codecov = parser.parse_args()
    
    return upload(url=codecov.url,
                  xml=codecov.xml, 
                  branch=codecov.branch, 
                  commit=codecov.commit, 
                  token=codecov.token,
                  **defaults)

def cli():
   print dumps(main())
   sys.exit(0) 

if __name__ == '__main__':
    cli()
