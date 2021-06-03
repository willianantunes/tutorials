using System;
using System.Collections.Generic;
using System.Linq;

namespace ItemsList.Business
{
    public class ShoppingPaper
    {
        private readonly List<SortedSet<String>> _listOfShoppingList;
        private readonly string _separator;

        public ShoppingPaper(string separator)
        {
            _separator = separator;
            _listOfShoppingList = new List<SortedSet<String>>();
        }

        public void InsertItemsToListNumber(string[] items, int listNumber)
        {
            // Create a list, if it's not available
            var possibleShoppingList = _listOfShoppingList.ElementAtOrDefault(listNumber);
            var shoppingList = possibleShoppingList is not null ? possibleShoppingList : new();
            // Fill it with items
            foreach (var item in items)
            {
                shoppingList.Add(item);
            }
            // Because when you create a new list, it must be inserted
            // No problem to replace in case of an existing one
            _listOfShoppingList.Insert(listNumber, shoppingList);
        }

        public string RetrieveItemsFromListNumber(int listNumber)
        {
            var shoppingList = _listOfShoppingList.ElementAt(listNumber);

            return String.Join(_separator, shoppingList);
        }
    }
}
