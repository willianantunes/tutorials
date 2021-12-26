using System;
using System.IO;
using ItemsList;
using Tests.Resources;
using Xunit;

namespace Tests
{
    public class ProgramTests
    {
        [Theory(DisplayName = "Should return ordered list of items without repetition given inputs")]
        [InlineData("sample-input-1.txt")]
        public void ShouldRetrieveListsGivenInputs(string sampleInput)
        {
            // Arrange
            using var willSimulateUserInput = Handler.ReadFileAsStreamReader(sampleInput);
            Console.SetIn(willSimulateUserInput);
            var reader = new StringWriter();
            Console.SetOut(reader);
            var mainArgument = new string[] { };
            // Act
            Program.Main(mainArgument);
            // Assert
            var result = reader.ToString();
            var expectedResult = "carne laranja picles suco\nlaranja pera\n";
            Assert.Equal(expectedResult, result);
        }
    }
}
