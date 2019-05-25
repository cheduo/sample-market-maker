#!/home/chenduo/anaconda3/bin/q
if[1 >= count system "pgrep -af marketmaker";
   -1"marketmaker reboot!"
   system "cd /home/chenduo/github/dj/sample-market-maker";
   system "/home/chenduo/github/dj/sample-market-maker/marketmaker&";
  ];
exit 0;
