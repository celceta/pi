#!/usr/local/bin/bash

### Start http response
echo 'Content-type: text/html; charset=utf-8'
echo

echo "<HTML>"

echo "<head>"

cat << EOF
 <style>
    /* タブのスタイル */
    .tabs {
      display: flex;
      border-bottom: 2px solid #ccc;
      width: 300px;
    }

    .tabs label {
      flex: 1;
      text-align: center;
      padding: 1em;
      background: #eee;
      cursor: pointer;
      font-weight: bold;
    }

    /* ラジオボタンを非表示に */
    input[name="tab"] {
      display: none;
    }

    /* 選択中のタブの見た目 */
    #tab1:checked ~ .tabs label[for="tab1"],
    #tab2:checked ~ .tabs label[for="tab2"] {
      background: #fff;
      border-bottom: 2px solid #007BFF;
    }

    /* テーブルの表示制御 */
    .content {
      display: none;
      padding: 1em;
    }

    #tab1:checked ~ #content1,
    #tab2:checked ~ #content2 {
      display: block;
    }

    table {
      width: *;
      border-collapse: collapse;
    }

    th, td {
      border: 1px solid #999;
      padding: 0.5em;
    }
  </style>
EOF


echo "</head>"

echo "<body>"
echo "<PRE>"; date; echo "</PRE>"


cat << EOF
  <input type="radio" name="tab" id="tab1" checked>
  <input type="radio" name="tab" id="tab2">
  <div class="tabs">
    <label for="tab1">1時間毎</label>
    <label for="tab2">10分毎</label>
  </div>
EOF

echo '<div id="content1" class="content">'
echo "<TABLE border width=\"*\">"
echo "<TR><TH>TIMESTAMP</TH><TH width=120>%</TH><TH>V</TH><TH>A</TH><TH width=120>W</TH></TR>"
mysql --defaults-extra-file=.mysql/mysql.conf -s -N -e "select * from ソーラー充電実績_1時間毎 order by TS_KEY desc limit 36" 2>&1 \
| awk -F'\t' '{
	p=$2 / 2; pw=50-p;
	if($5 < 0) { r=(-$5) / 10; g=0; } else { g=  $5  / 10; r=0; }
	w1=60-r; w2=60-g;
	printf("<TR align=\"right\">\
		<TH>%s</TH>\
		<TD>%.1f<BR><IMG SRC=\"green.png\" WIDTH=%d HEIGHT=8 /></TD>\
		<TD>%.2f</TD>\
		<TD>%.1f</TD>\
		<TD>%.0f<BR><IMG SRC=\"white.png\" WIDTH=%d HEIGHT=8 /><IMG SRC=\"red.png\"   WIDTH=%d HEIGHT=8 /><IMG SRC=\"green.png\" WIDTH=%d HEIGHT=8 /><IMG SRC=\"white.png\" WIDTH=%d HEIGHT=8 /></NOBR></TD>\
		</TR>\n", $1, $2, p, $3, $4, $5, w1, r, g, w2\
	);
}'
echo "</TABLE>"
echo "</div>"

echo '<div id="content2" class="content">'
echo "<TABLE border=1>"
echo "<TR><TH>TIMESTAMP</TH><TH width=120>%</TH><TH>V</TH><TH>A</TH><TH width=120>W</TH></TR>"
mysql --defaults-extra-file=.mysql/mysql.conf -s -N -e "select * from ソーラー充電実績_10分毎 order by TS_KEY desc limit 36" 2>&1 \
| awk -F'\t' '{
	p=$2 / 2; pw=50-p;
	if($5 < 0) { r=(-$5) / 10; g=0; } else { g=  $5  / 10; r=0; }
	w1=60-r; w2=60-g;
	printf("<TR align=\"right\">\
		<TH>%s</TH>\
		<TD>%.1f<BR><IMG SRC=\"green.png\" WIDTH=%d HEIGHT=8 /></TD>\
		<TD>%.2f</TD>\
		<TD>%.1f</TD>\
		<TD>%.0f<BR><IMG SRC=\"white.png\" WIDTH=%d HEIGHT=8 /><IMG SRC=\"red.png\"   WIDTH=%d HEIGHT=8 /><IMG SRC=\"green.png\" WIDTH=%d HEIGHT=8 /><IMG SRC=\"white.png\" WIDTH=%d HEIGHT=8 /></NOBR></TD>\
		</TR>\n", $1, $2, p, $3, $4, $5, w1, r, g, w2\
	);
}'
echo "</TABLE>"
echo "</div>"

echo "DONE"


cat << EOF
<script>
  // 初期復元
  window.addEventListener('DOMContentLoaded', () => {
    const lastTab = localStorage.getItem('selectedTab');
    if (lastTab) {
      const el = document.getElementById(lastTab);
      if (el) el.checked = true;
    }
  });

  // 各 input に直接イベントを付ける
  const tabInputs = document.querySelectorAll('input[name="tab"]');
  tabInputs.forEach(input => {
    input.addEventListener('change', () => {
      localStorage.setItem('selectedTab', input.id);
      console.log('saved', input.id);
    });
  });
</script>
EOF


echo "</body>"
echo "</HTML>"

exit 0
