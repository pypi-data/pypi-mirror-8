using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SimpleCalculator
{
    // The class which represents our calculator.
    [TestFixture]
    public class Calculator
    {
        public int Add(int a, int b)
        {
            return a + b;
        }

        public int Subtract(int a, int b)
        {
            return a - b;
        }

        public int Multiply(int a, int b)
        {
            // Intentional failure: the multiplication test will fail because this function is adding instead of multiplying.
            return a + b;
        }

        public int Divide(int a, int b)
        {
            return a / b;
        }

        public double Exponentiation(int a, int b)
        {
            // Intentional failure: the exponentiation test will fail because this function is always returning zero.
            return 0;
        }
    }
}
