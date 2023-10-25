#!/bin/bash
while ${prompt_for_exit}; do
        echo "*********************************"
        echo "*                               *"
        echo "*    Do you wish to exit        *"
        echo "*                               *"        
        echo "*(this will leave the system up)*"
        echo "*                               *"
        echo "*********************************"
        while true; do
            read -p "Do wish to kill exit? [y/n]:" yn
            case $yn in
                [Yy]* ) do_exit=1;break;;
                [Nn]* ) do_exit=0;break;;
                * ) echo "Please answer \"y\" or \"n\".";;
            esac
        done        
break
 
done


if [[ "$do_exit" -eq 1 ]]
then
echo "*********************************"
echo "*                               *"
echo "*        exiting                *"
echo "*                               *"
echo "*********************************"
export do_exit=$do_exit
fi
