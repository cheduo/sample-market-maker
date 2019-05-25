system "cd /home/chenduo/github/dj/sample-market-maker";
px_tab : ("PFFFF";1#csv) 0: read0`:XBTUSD_2019.05.19;
t: 1!px_tab
system "l d0.q";
.d0.plot t
// plt.plot[exec datetime from px_tab;flip px_tab`last`mid];
// plt.plot[exec datetime from px_tab;px_tab`mid];
// plt.plot[exec datetime from px_tab;px_tab`buy];
// plt.plot[exec datetime from px_tab;px_tab`sell];
// plt.xlabel"time (s)";
// plt.ylabel"px";
// plt.title "A chart created using q data";
// plt.grid 1b;
// plt.show[];
