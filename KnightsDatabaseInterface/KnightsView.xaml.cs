using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using Microsoft.Data.Sqlite;
using FilePath = System.IO.Path;   

namespace KnightsDatabaseInterface
{
    /// <summary>
    /// Interaction logic for KnightsView.xaml
    /// </summary>
    public partial class KnightsView : UserControl
    {
        private string dbFileName = "Data Source=ok_knights_directory.db";
        public KnightsView()
        {
            InitializeComponent();
            testBox.Text = TestKnight.FirstName + " " + TestKnight.LastName;
            string test = Environment.CurrentDirectory;
            string test2 = FilePath.Combine(test, dbFileName);

            using (var connection = new SqliteConnection(dbFileName))
            {
                connection.Open();
                var command = connection.CreateCommand();
                command.CommandText =
                    @"
                        SELECT * from knights
                    ";

                using(var reader = command.ExecuteReader())
                {
                    var names = new List<string>();
                    while(reader.Read())
                    {
                        names.Add(reader.GetString(0));
                    }
                    testBox.Text = names.First() + " " + TestKnight.LastName;
                }
            }
        }

        private Knight TestKnight = new()
        {
            FirstName = "Zak",
            MiddleName = "Anton",
            LastName = "Kastl",
            Address = "128 Fate St.",
            City = "Yukon",
            ZipCode = "73099",
            EmailAddress = "zak@zetacorp.com",
            Council = "6478",
            Roles = new string[] { "State Warden", "State Roundtable Chair" }
        };
    }
}
