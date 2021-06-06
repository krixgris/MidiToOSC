jsonData='
{
	"2/matrix/fader":1.0,
	"2/matrix/aux/4/send":0.0,
	"0/matrix/fader":1.0,
	"0/matrix/aux/4/send":0.0,
	"4/matrix/fader":1.0,
	"4/matrix/aux/4/send":0.0,
	"6/matrix/fader":1.0,
	"6/matrix/aux/4/send":0.0,
	"36/matrix/fader":1.0,
	"36/matrix/aux/4/send":0.0,
	"31/matrix/fader":1.0,
	"31/matrix/aux/4/send":0.0,
	"8/matrix/fader":1.0,
	"8/matrix/aux/4/send":0.0,
	"32/matrix/fader":1.0,
	"32/matrix/aux/4/send":0.0,
	"34/matrix/fader":1.0,
	"34/matrix/aux/4/send":0.0,
	"35/matrix/fader":1.0,
	"35/matrix/aux/4/send":0.0,
	"30/matrix/fader":1.0,
	"30/matrix/aux/4/send":0.0,
	"10/matrix/fader":1.0,
	"10/matrix/aux/4/send":0.0,
    "2/matrix/aux/0/send":0.0,
    "2/matrix/aux/2/send":0.0,
    "0/matrix/aux/0/send":0.0,
    "0/matrix/aux/2/send":0.0,
    "4/matrix/aux/0/send":0.0,
    "4/matrix/aux/2/send":0.0,
    "6/matrix/aux/0/send":0.0,
    "6/matrix/aux/2/send":0.0,
    "36/matrix/aux/0/send":0.0,
    "36/matrix/aux/2/send":0.0,
    "31/matrix/aux/0/send":0.0,
    "31/matrix/aux/2/send":0.0,
    "8/matrix/aux/0/send":0.0,
    "8/matrix/aux/2/send":0.0,
    "32/matrix/aux/0/send":0.0,
    "32/matrix/aux/2/send":0.0,
    "34/matrix/aux/0/send":0.0,
    "34/matrix/aux/2/send":0.0,
    "35/matrix/aux/0/send":0.0,
    "35/matrix/aux/2/send":0.0,
    "30/matrix/aux/0/send":0.0,
    "30/matrix/aux/2/send":0.0,
    "10/matrix/aux/0/send":0.0,
    "10/matrix/aux/2/send":0.0
}'

jsonParam="${jsonData//
/}"
jsonParam="${jsonParam//	/}"

jsonParam="${jsonParam//    /}"
echo "jsonParam='${jsonParam}'"

curl --data \
'json='$jsonParam \
192.168.1.167/datastore/mix/chan
