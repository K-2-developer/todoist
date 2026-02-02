

class BoardErrors:
    
    @staticmethod
    def not_found(self):
        return {'error': 'Board not found'}


def board_not_found():
    return None