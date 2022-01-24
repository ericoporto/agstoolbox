using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace AgsToolbox
{
    class ToolboxApplicationContext : ApplicationContext
    {
        private NotifyIcon trayIcon;
        private ContextMenuStrip contextMenuStripNotification;
        private ToolStripMenuItem toolStripMenuItemOpenToolbox;
        private ToolStripMenuItem toolStripMenuItemQuitToolbox;


        public ToolboxApplicationContext()
        {
            toolStripMenuItemOpenToolbox = new System.Windows.Forms.ToolStripMenuItem();
            toolStripMenuItemQuitToolbox = new System.Windows.Forms.ToolStripMenuItem();
            contextMenuStripNotification = new System.Windows.Forms.ContextMenuStrip();

            contextMenuStripNotification.ImageScalingSize = new System.Drawing.Size(20, 20);
            contextMenuStripNotification.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            toolStripMenuItemOpenToolbox,
            toolStripMenuItemQuitToolbox});
            contextMenuStripNotification.Name = "contextMenuStripNotification";
            contextMenuStripNotification.Size = new System.Drawing.Size(211, 80);
            // 
            // toolStripMenuItemOpenToolbox
            // 
            toolStripMenuItemOpenToolbox.Name = "toolStripMenuItemOpenToolbox";
            toolStripMenuItemOpenToolbox.Size = new System.Drawing.Size(210, 24);
            toolStripMenuItemOpenToolbox.Text = "Open Toolbox";
            toolStripMenuItemOpenToolbox.Click += new System.EventHandler(this.toolStripMenuItemOpenToolbox_Click);
            // 
            // toolStripMenuItemQuitToolbox
            // 
            toolStripMenuItemQuitToolbox.Name = "toolStripMenuItemQuitToolbox";
            toolStripMenuItemQuitToolbox.Size = new System.Drawing.Size(210, 24);
            toolStripMenuItemQuitToolbox.Text = "Quit Toolbox";
            toolStripMenuItemQuitToolbox.Click += new System.EventHandler(this.toolStripMenuItemQuitToolbox_Click);


            // Initialize Tray Icon
            trayIcon = new NotifyIcon()
            {
                BalloonTipText = "AGS Toolbox",
                Text = "AGS Toolbox",
                Icon = Resources.NotifyIconToolbox,
                ContextMenuStrip = contextMenuStripNotification,
                Visible = true
            };
        }

        private void toolStripMenuItemOpenToolbox_Click(object sender, EventArgs e)
        {
            var form = new ToolboxMain();
            form.Show();
        }

        private void toolStripMenuItemQuitToolbox_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        void Exit(object sender, EventArgs e)
        {
            // Hide tray icon, otherwise it will remain shown until user mouses over it
            trayIcon.Visible = false;

            Application.Exit();
        }
    }
}
