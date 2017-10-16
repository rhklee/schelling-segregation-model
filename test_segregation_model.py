import segregation_model
import unittest

def create_agent(atype):
    return { 'type': atype, 'satisfactionState': None }   
 
class TestSegregationModel(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.test_board_dim = 4
        self.test_board_types = [ 'A' ] * 7 + [ 'B' ] * 5 + [ '_' ] * 4
        self.test_board = [ \
            [ create_agent('A') ] * 4, \
            [ create_agent('A') ] * 3 + [ create_agent('B') ], \
            [ create_agent('B') ] * 4, \
            [ create_agent('_') ] * 4 ]
        self.test_str_board = "A A A A \n" + \
                              "A A A B \n" + \
                              "B B B B \n" + \
                              "_ _ _ _ "

    def test_create_nbhd_dims(self):
        neighborhood_dim = segregation_model.NBHD_DIM
        nbhd = segregation_model.create_nbhd(0.45, 0.45, neighborhood_dim)
        self.assertEqual(len(nbhd), neighborhood_dim)
        for row in nbhd:
            self.assertEqual(len(row), neighborhood_dim)

    def test_create_nbhd_value_error(self):
        with self.assertRaises(ValueError):
            segregation_model.create_nbhd(0.55, 0.5, 10)

    def test_create_agent_board(self):
        agent_board = segregation_model.create_agent_board(self.test_board_types, self.test_board_dim)
        self.assertEqual(agent_board, self.test_board)
    
    def test_stringify_board(self):
        """Test stringified board output."""
        self.assertEqual(segregation_model.stringify_board(self.test_board), self.test_str_board)
         

if __name__ == '__main__':
    unittest.main()


