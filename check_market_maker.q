#!/home/chenduo/anaconda3/bin/q
if[1 >= count system "pgrep -af marketmaker";
   -1"marketmaker reboot!"
   system "cd /home/chenduo/github/dj/dev_market_maker";
   system "/home/chenduo/github/dj/dev_market_maker/mymarketmaker&";
  ];
exit 0;
