using System;
using System.Linq;
using ItemsList.Business;

namespace ItemsList
{
    public class Program
    {
        private const string DefaultSeparator = " ";

        public static void Main(string[] args)
        {
            var numberOfListsToBeRead = int.Parse(Console.ReadLine());
            var shoppingPaper = new ShoppingPaper(DefaultSeparator);

            foreach (int listNumber in Enumerable.Range(0, numberOfListsToBeRead))
            {
                var providedRawListOfItems = Console.ReadLine();

                if (!String.IsNullOrEmpty(providedRawListOfItems))
                {
                    var cleanedRawList = providedRawListOfItems.Trim();
                    var items = cleanedRawList.Split(DefaultSeparator);
                    shoppingPaper.InsertItemsToListNumber(items, listNumber);
                }

                var result = shoppingPaper.RetrieveItemsFromListNumber(listNumber);
                Console.WriteLine(result);
            }
        }
    }
}
