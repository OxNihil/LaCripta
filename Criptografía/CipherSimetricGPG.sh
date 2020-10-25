#!/bin/bash

doc_ext=("txt" "rtf" "doc" "docs" "xls" "pdf" "html" "ppt" "pptx" "csv")
imag_ext=("png" "jpg" "bmp" "gif" "ttif" "svg")
vid_ext=("mp4" "flv" "avi" "webm" "mkv" "3gp" "vob" "wmv" "mpg" "m4v")
music_ext=("wav" "mp3" "wma")

doc=0
imag=0
vid=0
music=0
file=0

banner() {
	clear
	echo "~~~~~~~~~~~~~~~~~~~~~" 
 	echo " Cipher Simetric GPG "
 	echo "~~~~~~~~~~~~~~~~~~~~~"
}

help(){
	echo "Usage: ./CipherGPG [options] <paht>"
	echo "-c : Cipher"
	echo "-d : Decipher"
}

cipher(){
        FILE_NAME="$(basename "${entry}")"
        DIR="$(dirname "${entry}")"
        NAME="${FILE_NAME%.*}"
        EXT="${FILE_NAME##*.}"		
	output=""
	printf "[+]Encripting $FILE_NAME \n"
	if [ "$rename" -eq "0" ]; then
		gpg --symmetric --batch --passphrase $password $DIR/$FILE_NAME
		rm $DIR/$FILE_NAME 	
	elif [ "$rename" -eq "1" ]; then
		echo $doc_ext | grep -w $EXT > /dev/null
		if [ "$?" -eq "0" ]; then
			output="document$doc.$EXT" 
			let "doc++"
		fi
		echo $imag_ext | grep -w $EXT > /dev/null
		if [ "$?" -eq "0" ]; then
			output="imag$imag.$EXT" 
			let "imag++"
		fi
		echo $vid_ext | grep -w $EXT  > /dev/null
		if [ "$?" -eq "0" ]; then
			output="video$vid.$EXT"
			let "vid++"
		fi
		echo $music_ext | grep -w $EXT  > /dev/null
		if [ "$?" -eq "0" ]; then
			output="music$music.$EXT"
			let "music++"
		fi
		if [ "$output" = "" ]; then
			output="file$file.$EXT"
			let "file++"
		fi
		gpg --output "$DIR/$output.gpg" --symmetric --batch --passphrase $password $DIR/$FILE_NAME
		rm $DIR/$FILE_NAME
		

	fi
}

decipher(){
        FILE_NAME="$(basename "${entry}")"
        DIR="$(dirname "${entry}")"
        NAME="${FILE_NAME%.*}"
        EXT="${FILE_NAME##*.}"	
	printf "[+]Decripting $FILE_NAME \n"
	gpg -d --output $DIR/$NAME --batch --passphrase $password $DIR/$FILE_NAME 
	if [ "$?" -eq "0" ]; then 
		rm $DIR/$FILE_NAME 
	fi
}

reccipher(){
	for entry in $(find $ruta); do 
		if [ -f "$entry" ]; then 
			cipher
		fi
	done
}

recdecipher(){
	for entry in $(find $ruta -name *.gpg); do 
		if [ -f "$entry" ]; then 
			decipher
		fi
	done
}

#main execution

if [ "$#" -ne 2 ]; then
	echo ${RED}"[!]Invalid arguments"${STD}
	echo ""	
	help
	exit 0;
fi
ruta=$2
option=$1
read -p "Introduce la clave de cifrado: " password 
if [ "$password" = "" ];then
	echo "[!]Clave no valida"
	exit 0;
fi
if [[ "$1" = "-c" || "$1" = "-C" ]]; then
	read -p "¿Deseas renombrar de forma generica los ficheros? [y/n] (N default) : " rename
	case $rename in
		y|Y)
		        rename=1;;
		n|N)
		        rename=0;;
		*)
		        rename=0;;
	esac
	echo ""
	reccipher
elif [[ "$1" = "-d" || "$1" = "-D" ]]; then
	recdecipher		
fi


