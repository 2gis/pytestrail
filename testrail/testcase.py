class TestRailTestCase:
    def __init__(self, title, section, suite, steps):
        self.title = title
        self.section_name = section
        self.suite_name = suite
        self.steps = steps
        self.type_id = 1
        self.priority_id = 4

    def to_json_dict(self):
        return {
            'title': self.title,
            'type_id': self.type_id,
            'priority_id': self.priority_id,
            'custom_steps_separated': self.steps
        }
