import unittest
from project_euler.problem_124.sol1 import solution

class TestEuler124(unittest.TestCase):
    def test_solution(self):
        # Testes básicos fornecidos no problema
        self.assertEqual(solution(10, 6), 9)
        self.assertEqual(solution(10, 9), 7)
        self.assertEqual(solution(100000, 10000), 21417)

    def test_small_cases(self):
        # Testes com valores pequenos de n_max e k
        self.assertEqual(solution(5, 1), 1)
        self.assertEqual(solution(5, 3), 4)
        self.assertEqual(solution(10, 4), 8)

    def test_edge_cases(self):
        # Testes com valores de borda
        self.assertEqual(solution(1, 1), 1)  
        self.assertEqual(solution(10, 10), 10)  

    def test_large_cases(self):
        # Testes com valores maiores
        self.assertEqual(solution(1000, 500), 801) 

    def test_performance(self):
        # Teste de desempenho para valores grandes
        result = solution(10000, 5000)
        self.assertTrue(result > 0)  

if __name__ == "__main__":
    unittest.main()