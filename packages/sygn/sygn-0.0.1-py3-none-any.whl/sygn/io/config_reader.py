from pathlib import Path

import yaml
from astropy import units as u


class ConfigReader():
    """Class to io configuration files.
    """

    def __init__(self, path_to_config_file: Path):
        """Constructor method.
        :param path_to_config_file: Path to the configuration file.
        """
        self.path_to_config_file = path_to_config_file
        self._config_dict = dict()
        self._read_raw_config_file()

    def _read_raw_config_file(self):
        """Read the configuration file and save its content in a dictionary.
        """
        with open(self.path_to_config_file, 'r') as config_file:
            self._config_dict = yaml.load(config_file, Loader=yaml.SafeLoader)

    def _parse_units(self):
        """Parse the units of the numerical parameters and convert them to astropy quantities.
        """
        for key in self._config_dict.keys():
            for subkey in self._config_dict[key]:
                try:
                    self._config_dict[key][subkey] = u.Quantity(self._config_dict[key][subkey])
                except TypeError:
                    for subsubkey in self._config_dict[key][subkey]:
                        try:
                            self._config_dict[key][subkey][subsubkey] = u.Quantity(
                                self._config_dict[key][subkey][subsubkey])
                        except TypeError:
                            pass

    def get_config_from_file(self) -> dict():
        """Return a dictionary containing the content of the configuration file.

        :return: A dictionary with the configurations.
        """
        return self._config_dict
