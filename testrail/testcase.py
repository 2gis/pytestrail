class TestRailTestCase:
    def __init__(self, name, section, suite, steps):
        self.name = name
        self.section_name = section
        self.suite_name = suite
        self.steps = steps

    def to_json_dict(self):
        jobject = {
            'title': self.name,
            'type_id': 1,
            'priority_id': 4,
            'custom_steps_separated': self.steps
        }

        return jobject