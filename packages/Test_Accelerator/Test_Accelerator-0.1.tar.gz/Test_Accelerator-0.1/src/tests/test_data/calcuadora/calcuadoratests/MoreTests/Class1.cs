using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using NUnit.Framework;
using SimpleCalculator;

namespace MoreCalcTests.Foo.Bar
{
    [TestFixture]
    public class CalculatorTests4
    {
        // The calculator object that will be used by the tests to verify the Calculator class funcionalities.
        private Calculator _calculator;

        [TestFixtureSetUp]
        public void Initialize()
        {
            _calculator = new Calculator();
        }

        [Test]
        public void Add_Test()
        {
            // Setup the values to be used by this test.
            int a = 10;
            int b = 20;
            int expectedSum = (a + b);

            // Exercises the sum functionality of the calculator.
            int actualSum = _calculator.Add(a, b);

            // Checks if the sum was performed correctly.
            Assert.AreEqual(expectedSum, actualSum, "The sum function of the calculator did not return the expected value.");
        }

        [Test]
        public void Subtraction_Test()
        {
            // Defines the values ​​to be used by this test.
            int a = 10;
            int b = 7;
            int expectedDifference = (a - b);

            // Exercises the subtraction functionality of the calculator.
            int actualDifference = _calculator.Subtract(a, b);

            // Checks if the subtraction was performed correctly.
            Assert.AreEqual(expectedDifference, actualDifference, "The subtraction function of the calculator did not return the expected value.");
        }

        [Test]
        public void Multiplication_Test()
        {
            // Defines the values ​​to be used by this test.
            int a = 2;
            int b = 3;
            int expectedProduct = (a * b);

            // Exercises the multiplication functionality of the calculator.
            int actualProduct = _calculator.Multiply(a, b);

            // Verifies if the subtraction was performed correctly.
            Assert.AreEqual(expectedProduct, actualProduct, "The multiplication function of the calculator did not return the expected value.");
        }

        [Test]
        public void Divide_Test()
        {
            // Setup the values ​​to be used by this test.
            int a = 50;
            int b = 10;
            int expectedResult = (a / b);

            // Exercises the Divide functionality of the calculator.
            int actualResult = _calculator.Divide(a, b);

            // Checks if the division was performed correctly.
            Assert.AreEqual(expectedResult, actualResult, "The divide function of the calculator did not return the expected value.");
        }

        [Test]
        public void Exponentiation_Test()
        {
            Assert.AreEqual(1, _calculator.Exponentiation(5, 0), "The exponentiation function of the calculator is not working correctly.");
            Assert.AreEqual(5, _calculator.Exponentiation(5, 1), "The exponentiation function of the calculator is not working correctly.");
            Assert.AreEqual(25, _calculator.Exponentiation(5, 2), "The exponentiation function of the calculator is not working correctly.");
            Assert.AreEqual(0.2, _calculator.Exponentiation(5, -1), "The exponentiation function of the calculator is not working correctly.");
        }
    }
}
