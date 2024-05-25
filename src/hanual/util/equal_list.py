from __future__ import annotations


class ItemEqualList(list):
    def __contains__(self, item):
        for element in self:
            if element == item:
                return True

        return False
