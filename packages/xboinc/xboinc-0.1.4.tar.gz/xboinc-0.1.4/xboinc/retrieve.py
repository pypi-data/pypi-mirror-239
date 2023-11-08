# copyright ############################### #
# This file is part of the Xboinc Package.  #
# Copyright (c) CERN, 2023.                 #
# ######################################### #

import json
from pathlib import Path

from .user import get_domain, get_folder
from .server.eos import mv_from_eos, mv_to_eos, xrdcp_installed
from .server.afs import mv_from_afs, mv_to_afs
from .server.tools import untar
from .simulation_io import SimState


class RetrieveJobs:

    def __init__(self, user, study):
        self._user      = user
        self._study     = study
        self._directory = get_folder(user) / "output"
        self._to_delete = []
        for tar_file in self._directory.glob('*.tar.gz'):
            untar(tar_file)


    def _clean(self):
        for json_file in self._to_delete:
            json_file.with_suffix('.bin').unlink()
            json_file.unlink()
        # Delete empty folders
        for folder in self._directory.glob('*/'):
            if not any(folder.iterdir()):
                folder.rmdir()


    def __iter__(self):
        json_files = []
        for json_file in self._directory.glob('*/*.json'):
            with open(json_file, 'r') as json_file_obj:
                json_content = json.load(json_file_obj)
            if json_content.get("study") == self._study and json_content.get("user") == self._user:
                json_files.append(json_file)
        json_files = set(json_files) - set(self._to_delete)
        if not json_files:
            print(f"Warning: No JSON files found in {self._directory} for {self._user} study {self._study}.")
        self._json_files = iter(json_files)
        return self


    def __next__(self):
        try:
            json_file = next(self._json_files)
        except StopIteration:
            self._clean()
            raise StopIteration
        else:
            bin_file = json_file.with_suffix('.bin')
            try:
                with open(json_file, 'r') as json_file_obj:
                    json_content = json.load(json_file_obj)
                result    = SimState.from_binary(bin_file)
                particles = result.particles
            except Exception as e:
                print(f"Error loading binary file {bin_file}: {e}")
            else: 
                self._to_delete.append(json_file)
                return json_content, particles

