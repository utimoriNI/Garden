using System;
using System.IO;
using System.Text;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;
using System.Web.Script.Serialization;

// Native Windows app: no console, URI handler, or external shell at launch.
internal static class ObsidianTaskLauncher
{
    private static readonly UTF8Encoding Utf8 = new UTF8Encoding(false);

    [STAThread]
    private static int Main(string[] args)
    {
        string vault = null;
        string task = null;
        for (int i = 0; i < args.Length; i++)
        {
            if (args[i] == "--vault" && i + 1 < args.Length) vault = args[++i];
            else if (args[i] == "--text" && i + 1 < args.Length) task = args[++i];
            else return 2;
        }
        try
        {
            if (vault == null)
                vault = File.ReadAllText(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "vault-path.txt"), Utf8).Trim();
            if (task != null)
            {
                if (!String.IsNullOrWhiteSpace(task)) Console.WriteLine(AppendTask(vault, task));
                return 0;
            }
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            using (var form = new Form())
            {
                form.Text = "Obsidian タスク追加";
                form.ClientSize = new Size(540, 140);
                form.FormBorderStyle = FormBorderStyle.FixedDialog;
                form.MaximizeBox = false;
                form.MinimizeBox = false;
                form.StartPosition = FormStartPosition.CenterScreen;
                form.TopMost = true;
                form.Font = new Font("Segoe UI", 10);
                var label = new Label { Text = "タスク本文を入力してください。#📎Task は自動で付きます。", AutoSize = true, Location = new Point(16, 15) };
                var input = new TextBox { Location = new Point(16, 43), Width = 508 };
                var add = new Button { Text = "追加", Location = new Point(335, 91), Width = 90 };
                var cancel = new Button { Text = "キャンセル", Location = new Point(434, 91), Width = 90, DialogResult = DialogResult.Cancel };
                form.Controls.AddRange(new Control[] { label, input, add, cancel });
                form.AcceptButton = add;
                form.CancelButton = cancel;
                form.Shown += delegate { input.Focus(); };
                add.Click += delegate
                {
                    if (String.IsNullOrWhiteSpace(input.Text)) { input.Focus(); return; }
                    try { AppendTask(vault, input.Text); form.Close(); }
                    catch (Exception ex) { MessageBox.Show(form, ex.Message, "タスクを追加できませんでした", MessageBoxButtons.OK, MessageBoxIcon.Error); }
                };
                form.ShowDialog();
            }
            return 0;
        }
        catch (Exception ex)
        {
            if (task != null) Console.Error.WriteLine(ex.Message);
            else MessageBox.Show(ex.Message, "タスク追加の起動エラー", MessageBoxButtons.OK, MessageBoxIcon.Error);
            return 1;
        }
    }

    private static string Value(Dictionary<string, object> config, string key)
    {
        object value;
        return config.TryGetValue(key, out value) && value != null ? value.ToString() : "";
    }

    private static string AppendTask(string vault, string task)
    {
        if (task.IndexOfAny(new char[] { '\r', '\n' }) >= 0) throw new Exception("タスクは1行で入力してください。");
        string root = Path.GetFullPath(vault).TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar);
        var config = new JavaScriptSerializer().Deserialize<Dictionary<string, object>>(File.ReadAllText(Path.Combine(root, ".obsidian", "daily-notes.json"), Utf8));
        string format = Value(config, "format");
        if (format != "" && format != "YYYY-MM-DD") throw new Exception("YYYY-MM-DD形式のデイリーノートに対応しています。");
        var day = DateTime.Now;
        string name = day.ToString("yyyy-MM-dd");
        string folder = Path.GetFullPath(Path.Combine(root, Value(config, "folder")));
        if (folder != root && !folder.StartsWith(root + Path.DirectorySeparatorChar, StringComparison.OrdinalIgnoreCase))
            throw new Exception("デイリーノートの保存先がVaultの外になっています。");
        string path = Path.Combine(folder, name + ".md");
        string seed = "";
        string template = Value(config, "template");
        if (!File.Exists(path) && template != "")
        {
            string source = Path.Combine(root, template);
            if (Path.GetExtension(source) == "") source += ".md";
            seed = File.ReadAllText(source, Utf8)
                .Replace("<% tp.date.now(\"YYYY-MM-DD\", -1, tp.file.title, \"YYYY-MM-DD\") %>", day.AddDays(-1).ToString("yyyy-MM-dd"))
                .Replace("<% tp.date.now(\"YYYY-MM-DD\", 1, tp.file.title, \"YYYY-MM-DD\") %>", day.AddDays(1).ToString("yyyy-MM-dd"))
                .Replace("{{date}}", name).Replace("{{time}}", day.ToString("HH:mm")).Replace("{{title}}", name);
            if (seed.Contains("<%") || System.Text.RegularExpressions.Regex.IsMatch(seed, "\\{\\{.+?\\}\\}"))
                throw new Exception("未対応のテンプレート記法があります。Obsidianで今日のノートを先に作成してください。");
        }
        Directory.CreateDirectory(folder);
        FileStream stream = null;
        for (int attempt = 0; attempt < 10; attempt++)
        {
            try { stream = new FileStream(path, FileMode.OpenOrCreate, FileAccess.ReadWrite, FileShare.Read); break; }
            catch (IOException) { if (attempt == 9) throw; System.Threading.Thread.Sleep(100); }
        }
        using (stream)
        {
            if (stream.Length == 0 && seed != "") Write(stream, seed.TrimEnd('\r', '\n') + "\r\n");
            string separator = "";
            if (stream.Length > 0)
            {
                stream.Seek(-1, SeekOrigin.End);
                if (stream.ReadByte() != 10) separator = "\r\n";
            }
            stream.Seek(0, SeekOrigin.End);
            Write(stream, separator + "- [ ] #📎Task " + task.Trim() + "\r\n");
            stream.Flush();
        }
        return path;
    }

    private static void Write(FileStream stream, string text)
    {
        var bytes = Utf8.GetBytes(text);
        stream.Write(bytes, 0, bytes.Length);
    }
}
