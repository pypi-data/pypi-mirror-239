function stars(c,a,b){if(b.templateMode=='loading'){a=b.templateLoading(a);}else if(b.templateMode=='error'){a=b.templateError(a);}c.dataset.level=a;c.querySelectorAll("span").forEach(function(c,d){if(d<a){c.style.color=b.color;}else{c.style.color='';}});}