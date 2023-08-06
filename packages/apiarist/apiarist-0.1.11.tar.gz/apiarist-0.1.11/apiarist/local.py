# Copyright 2014 Max Sharples
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Class to manage local job execution
"""
import os
import subprocess
import hashlib
import time
import shutil
import logging
from apiarist.script import generate_hive_script_file, get_script_file_location

logger = logging.getLogger(__name__)


class LocalRunner():
    """
    Handles running the Hive script on
    a local Hive installation.
    """

    def __init__(self, job_name=None,
                 input_path=None, hive_query=None, output_dir=None,
                 temp_dir=None, no_output=False, retain_hive_table=False):

        #  TODO test for Hive installation

        self.job_name = job_name
        self.job_id = self._generate_job_id()
        self.start_time = time.time()

        # I/O for job data
        self.scratch_dir = self.get_local_scratch_dir(temp_dir)
        self.stream_output = (not no_output)

        self.data_path = self.scratch_dir + 'data'
        self.table_path = self.scratch_dir + 'table'
        self.input_path = os.path.abspath(input_path)
        if output_dir:
            self.output_dir = os.path.abspath(output_dir) + '/' + self.job_id
        else:
            self.output_dir = self.scratch_dir + 'output'

        # the Hive script object
        self.hive_query = hive_query
        self.local_script_file = get_script_file_location(self.job_id,
                                                          self.scratch_dir)
        self.retain_hive_table = retain_hive_table

    def get_local_scratch_dir(self, temp_dir=None):
        if temp_dir:
            tmp_path = temp_dir + self.job_id + '/'
        elif 'APIARIST_TMP_DIR' in os.environ:
            tmp_path = os.environ['APIARIST_TMP_DIR'] + self.job_id + '/'
        else:
            tmp_path = "{0}/.apiarist/{1}/".format(os.environ['HOME'],
                                                   self.job_id)
        return tmp_path

    def _ensure_local_scratch_dir_exists(self):
        if not os.path.exists(self.scratch_dir):
            os.makedirs(self.scratch_dir)

    def run(self):
        """
        Run the hive query against a local hive installation (*nix only)
        """
        # prepare files
        self._ensure_local_scratch_dir_exists()
        self._copy_input_data()
        self._generate_hive_script()
        # execute against local hive server
        cmd = ["hive -f {}".format(self.local_script_file)]
        logger.info("running HIVE script with: {}".format(cmd))
        hql = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        stdout = hql.communicate()
        if stdout[1] is not None:
            logger.info(stdout)
        # observe and report
        self._wait_for_job_to_complete()

    def _copy_input_data(self):
        shutil.copyfile(self.input_path, self.data_path)

    def _wait_for_job_to_complete(self):
        # TODO - wait until there are files in this dir
        cmd = ["cat {}/*".format(self.output_dir)]
        cat = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, shell=True)
        stdout, stderr = cat.communicate()
        if self.stream_output:
            logger.info("\nQuery output ------->\n")
            print(stdout)  # query results to STDOUT

    def _generate_hive_script(self):
        """
        Write the HQL to a local (temp) file
        """
        hq = self.hive_query.local_hive_script(self.data_path,
                                               self.output_dir,
                                               self.table_path)
        generate_hive_script_file(hq, self.local_script_file)

    def _generate_job_id(self):
        """
        Create a unique job run identifier
        """
        run_id = self.job_name + str(time.time())
        digest = hashlib.md5(run_id).hexdigest()
        return 'hj-' + digest

    #  hooks for the with statement ###

    def __enter__(self):
        """
        Don't do anything special at start of with block
        """
        s = self
        return s

    def __exit__(self, type, value, traceback):
        """
        Call self.cleanup() at end of with block.
        """
        self.cleanup()

    def cleanup(self):
        """
        cleanup the temp/scratch files that are
        used to set up the hive tables
        """
        if not self.retain_hive_table:
            os.remove(self.local_script_file)
            shutil.rmtree(self.scratch_dir)
