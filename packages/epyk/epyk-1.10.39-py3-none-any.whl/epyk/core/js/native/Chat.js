function chat(e,c,d){var b=document.createElement("p");b.style.margin="0 0 5px 0";if(d.showdown){var h=new showdown.Converter(d.showdown);c=h.makeHtml(c.trim());};b.innerHTML=c;e.querySelector("div").prepend(b);var f=new Date();var g=moment(f).format('YYYY-MM-DD HH:mm:ss');var a=document.createElement("p");a.style.margin=0;a.style.fontWeight='bold';a.innerHTML=g;e.querySelector("div").prepend(a);}