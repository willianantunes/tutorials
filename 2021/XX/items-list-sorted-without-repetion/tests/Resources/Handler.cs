using System;
using System.IO;

namespace Tests.Resources
{
    public class Handler
    {
        private static string _currentDirectory =
            Path.GetFullPath($"{Directory.GetParent(Environment.CurrentDirectory).Parent.FullName}../../Resources");

        public static StreamReader ReadFileAsStreamReader(string resourceToBeRead)
        {
            return new($"{_currentDirectory}/{resourceToBeRead}");
        }
    }
}
