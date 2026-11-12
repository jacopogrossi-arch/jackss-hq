// ffmpeg.cs: tramite per ffmpeg (HyperFrames lo trova con HYPERFRAMES_FFMPEG_PATH).
// HyperFrames 0.9.35 estrae i fotogrammi del video con (numero di core / 2) ffmpeg insieme, senza opzione per ridurli:
// su un 4K, 6 estrazioni insieme mandano in affanno RAM e disco e i suoi controlli a tempo fisso (30 s) scadono.
// Qui le sole estrazioni di fotogrammi (argomento -start_number) aspettano un posto: al massimo HF_EXTRACT_SLOTS insieme (default 2).
// Tutto il resto passa subito a ffmpeg vero (HF_REAL_FFMPEG). Il figlio eredita stdin/stdout/stderr e muore col tramite (job object).
using System; using System.Diagnostics; using System.Runtime.InteropServices; using System.Text; using System.Threading; using System.IO; using System.Collections.Generic;
class P {
  [DllImport("kernel32.dll", CharSet = CharSet.Unicode)] static extern IntPtr CreateJobObject(IntPtr a, string n);
  [DllImport("kernel32.dll")] static extern bool SetInformationJobObject(IntPtr h, int c, IntPtr p, uint l);
  [DllImport("kernel32.dll")] static extern bool AssignProcessToJobObject(IntPtr j, IntPtr p);
  [StructLayout(LayoutKind.Sequential)] struct BASIC { public long a, b; public uint LimitFlags; public UIntPtr c, d; public uint e; public UIntPtr f; public uint g, h; }
  [StructLayout(LayoutKind.Sequential)] struct IOC { public ulong a, b, c, d, e, f; }
  [StructLayout(LayoutKind.Sequential)] struct EXT { public BASIC Basic; public IOC Io; public UIntPtr a, b, c, d; }
  static string Q(string a) { if (a.Length > 0 && a.IndexOfAny(new[]{' ','\t','"'}) < 0) return a;
    var sb = new StringBuilder("\""); int bs = 0;
    foreach (char c in a) { if (c == '\\') { bs++; continue; } if (c == '"') { sb.Append('\\', bs * 2 + 1); sb.Append('"'); bs = 0; continue; } sb.Append('\\', bs); bs = 0; sb.Append(c); }
    sb.Append('\\', bs * 2); sb.Append('"'); return sb.ToString(); }
  static void L(string m) { try { var lf = Environment.GetEnvironmentVariable("HF_FFMPEG_LOG"); if (lf != null) File.AppendAllText(lf, DateTime.Now.ToString("HH:mm:ss.fff") + " [" + Process.GetCurrentProcess().Id + "] " + m + "\n"); } catch (Exception) { } }
  static int Main(string[] a) {
    bool extract = Array.IndexOf(a, "-start_number") >= 0;
    Semaphore sem = null; bool held = false;
    try {
      if (extract) { int n = 2; int.TryParse(Environment.GetEnvironmentVariable("HF_EXTRACT_SLOTS") ?? "2", out n); if (n < 1) n = 1;
        sem = new Semaphore(n, n, "hf-extract-slots-" + n); L("ATTESA " + string.Join(" ", a)); sem.WaitOne(); held = true; L("PARTE"); }
      var sb2 = new StringBuilder(); foreach (var x in a) { if (sb2.Length > 0) sb2.Append(' '); sb2.Append(Q(x)); }
      var psi = new ProcessStartInfo(Environment.GetEnvironmentVariable("HF_REAL_FFMPEG") ?? "ffmpeg.exe", sb2.ToString()) { UseShellExecute = false, RedirectStandardError = extract };
      var tail = new Queue<string>();
      using (var p = Process.Start(psi)) {
        if (extract) { p.ErrorDataReceived += (o, e) => { if (e.Data == null) return; Console.Error.Write(e.Data + "\n"); lock (tail) { tail.Enqueue(e.Data); if (tail.Count > 6) tail.Dequeue(); } }; p.BeginErrorReadLine(); }
        try { IntPtr job = CreateJobObject(IntPtr.Zero, null); var info = new EXT(); info.Basic.LimitFlags = 0x2000; // KILL_ON_JOB_CLOSE
          int len = Marshal.SizeOf(typeof(EXT)); IntPtr ptr = Marshal.AllocHGlobal(len); Marshal.StructureToPtr(info, ptr, false);
          SetInformationJobObject(job, 9, ptr, (uint)len); AssignProcessToJobObject(job, p.Handle); } catch (Exception) { }
        p.WaitForExit(); if (extract) { lock (tail) L("FINE exit " + p.ExitCode + " dopo " + (int)(DateTime.Now - p.StartTime).TotalSeconds + " s | " + string.Join(" || ", tail.ToArray())); } return p.ExitCode; }
    } finally { if (held) try { sem.Release(); } catch (Exception) { } }
  }
}
