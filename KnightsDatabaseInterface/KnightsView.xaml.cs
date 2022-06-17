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

namespace KnightsDatabaseInterface
{
    /// <summary>
    /// Interaction logic for KnightsView.xaml
    /// </summary>
    public partial class KnightsView : UserControl
    {
        public KnightsView()
        {
            InitializeComponent();
        }

        private Knight TestKnight = new Knight()
        {
            FirstName = "Zak",
            LastName = "Anton",
            Address = "128 Fate St.",
            City = "Yukon",
            ZipCode = "73099",
            EmailAddress = "zak@zetacorp.com",
            Council = "6478",
            Roles = new string[] { "State Warden", "State Roundtable Chair" }
        };
    }
}
