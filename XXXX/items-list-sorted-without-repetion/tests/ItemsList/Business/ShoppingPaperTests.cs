using ItemsList.Business;
using Xunit;

namespace Tests.Business
{
    public class BrainTests
    {
        private string _separator = " ";

        [Fact]
        public void ShouldAddTwoItemsListOne()
        {
            // Arrange
            var listOneIndex = 0;
            var paper = new ShoppingPaper(_separator);
            var listOfItems = new string[] {"piano", "potato"};
            // Act
            paper.InsertItemsToListNumber(listOfItems, listOneIndex);
            var rawItems = paper.RetrieveItemsFromListNumber(listOneIndex);
            // Assert
            Assert.Equal("piano potato", rawItems);
        }

        [Fact]
        public void ShouldAddFiveItemsListOneAndFiveItemsListTwo()
        {
            // Arrange
            var listOneIndex = 0;
            var listTwoIndex = 1;
            var paper = new ShoppingPaper(_separator);
            var listOneOfItems = new string[] {"carne", "laranja", "suco", "picles", "laranja", "picles"};
            var listTwoOfItems = new string[] {"laranja", "pera", "laranja", "pera", "pera"};
            // Act
            paper.InsertItemsToListNumber(listOneOfItems, listOneIndex);
            paper.InsertItemsToListNumber(listTwoOfItems, listTwoIndex);
            var rawItemsFromListOne = paper.RetrieveItemsFromListNumber(listOneIndex);
            var rawItemsFromListTwo = paper.RetrieveItemsFromListNumber(listTwoIndex);
            // Assert
            Assert.Equal("carne laranja picles suco", rawItemsFromListOne);
            Assert.Equal("laranja pera", rawItemsFromListTwo);
        }
    }
}
