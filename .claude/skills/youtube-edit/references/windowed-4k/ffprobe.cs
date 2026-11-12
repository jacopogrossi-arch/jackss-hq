// ffprobe.cs: tramite per ffprobe (HyperFrames lo trova con FFPROBE_PATH).
// HyperFrames 0.9.35 chiede "qual e' il keyframe prima di T" a ogni blocco di estrazione e uccide ffprobe dopo 30 s:
// su un 4K da 8 GB, con il disco sotto carico, sfora. Qui la risposta viene dalla lista gia' calcolata (HF_KEYFRAMES_FILE,
// una riga per keyframe, valida per il file HF_KEYFRAMES_FOR). Ogni altra richiesta passa a ffprobe vero (HF_REAL_FFPROBE).
using System; using System.Diagnostics; using System.Globalization; using System.IO; using System.Text;
class P {
  static string Q(string a) { if (a.Length > 0 && a.IndexOfAny(new[]{' ','\t','"'}) < 0) return a;
    var sb = new StringBuilder("\""); int bs = 0;
    foreach (char c in a) { if (c == '\\') { bs++; continue; } if (c == '"') { sb.Append('\\', bs * 2 + 1); sb.Append('"'); bs = 0; continue; } sb.Append('\\', bs); bs = 0; sb.Append(c); }
    sb.Append('\\', bs * 2); sb.Append('"'); return sb.ToString(); }
  static void L(string m) { try { var lf = Environment.GetEnvironmentVariable("HF_FFPROBE_LOG"); if (lf != null) File.AppendAllText(lf, DateTime.Now.ToString("HH:mm:ss.fff") + " " + m + "\n"); } catch (Exception) { } }
  static int Main(string[] a) {
    var inv = CultureInfo.InvariantCulture; L("IN  " + string.Join(" ", a));
    try {
      string kf = Environment.GetEnvironmentVariable("HF_KEYFRAMES_FILE"), forf = Environment.GetEnvironmentVariable("HF_KEYFRAMES_FOR");
      string ri = null; bool pk = false;
      for (int i = 0; i < a.Length; i++) { if (a[i] == "-read_intervals" && i + 1 < a.Length) ri = a[i + 1]; if (a[i] == "packet=pts_time") pk = true; }
      if (kf != null && forf != null && pk && ri != null && ri.EndsWith("%+#1") && a.Length > 0 &&
          string.Equals(Path.GetFileName(a[a.Length - 1]), Path.GetFileName(forf), StringComparison.OrdinalIgnoreCase) &&
          new FileInfo(a[a.Length - 1]).Length == new FileInfo(forf).Length) {
        double t = double.Parse(ri.Substring(0, ri.Length - 4), inv), best = double.NaN;
        foreach (var l in File.ReadAllLines(kf)) { double k; if (double.TryParse(l.Trim().TrimEnd(','), NumberStyles.Float, inv, out k) && k <= t + 1e-6) best = k; }
        if (!double.IsNaN(best)) { Console.Out.Write(best.ToString("F6", inv) + "\n"); L("LISTA " + best.ToString("F6", inv)); return 0; }
      }
    } catch (Exception e) { L("ECCEZIONE " + e.Message); }
    var sb2 = new StringBuilder(); foreach (var x in a) { if (sb2.Length > 0) sb2.Append(' '); sb2.Append(Q(x)); }
    var psi = new ProcessStartInfo(Environment.GetEnvironmentVariable("HF_REAL_FFPROBE") ?? "ffprobe.exe", sb2.ToString()) { UseShellExecute = false };
    using (var p = Process.Start(psi)) { p.WaitForExit(); L("VERO exit " + p.ExitCode); return p.ExitCode; }
  }
}
