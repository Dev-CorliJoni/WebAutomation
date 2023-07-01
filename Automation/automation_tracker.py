class AutomationTracker:

    def __init__(self, configuration_path, additional_information=False):
        self.additional_information = additional_information

        self.configuration_path = configuration_path

        self._website = ""
        self._current_configuration_number = 0
        self._current_step = 0

        if self.additional_information:
            self._website_stack = []

    @property
    def configuration_filename(self):
        return self.configuration_path.split("/")[-1]

    def changed_configuration(self, website):
        self._website = website
        self._current_configuration_number = self._current_configuration_number + 1
        self._current_step = 0

        if self.additional_information:
            self._website_stack.append([self.configuration_filename, website, self._current_configuration_number, self._current_step])

    def step_successful(self):
        self._current_step = self._current_step + 1

        if self.additional_information:
            self._update_website_stack(current_step=self._current_step)

    def _update_website_stack(self, **kwargs):
        indices = {
            "configuration_filename": 0,
            "website": 1,
            "current_configuration_level": 2,
            "current_step": 3
        }

        for key, val in kwargs.items():
            if val is not None:
                self._website_stack[-1][indices[key]] = val

    def __str__(self):
        _str = "[Automation Process]:\n"

        if self._current_configuration_number > 0:
            _format = "|-[{config_number}. {config_filename}](Website: {website}) Successfully executed steps: {step_number}.\n"

            if self.additional_information:

                for item in self._website_stack[:-1]:
                    _str = _str + _format.format(config_filename=item[0], website=item[1], config_number=item[2], step_number=item[3])

            website = "No Website" if self._website is None else self._website
            current_step = self._current_step-1 if self._current_step > 0 else 0

            _str = _str + _format.format(config_filename=self.configuration_filename, website=website,
                                         config_number=self._current_configuration_number, step_number=current_step)
        else:
            _str = _str + "|- Nothing started until now "

        return _str[:-1]