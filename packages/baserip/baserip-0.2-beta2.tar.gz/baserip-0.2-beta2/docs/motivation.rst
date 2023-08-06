.. _motivation:

Motivation For Creating Baserip
===============================

It's Christmas day 2013 and I'm up early. That's no surprise;
my ten year old daughter is *desperate* to unwrap her presents and 
she sits in front of me in the middle of a pile of promising wrappers, 
the only thing on her mind is which to open first.

At once she starts to look avidly through the small mountain, now where is
it? Aha, here it is! This is the one, somehow she detects the exotic
nature of the paper, its very foreigness. "This is the one" she gleefully
pronouces and she's correct. In the way that only children can, she has 
recognised the package from her uncle who lives far away from these
shores.

The paper surrounding the selected present yields as quickly as the snow 
melting outside the house. Inside she pulls out the long-awaited
package, her excitiment seeming to spark in her young eyes.

You see, my daughter is a **huge** fan of Harry Potter; she's read all
the books, many more than once, she's seen all the movies, well all 
except the one she's holding in her hands. This is the last film of
the series, the one she's been waiting for for so many months.

"Can we watch it Daddy!", I have to temper her excitment, "Later" I 
say with a smile and I know that I'll have to stick to my word.

And I do.

It is later and we put the DVD in the player and ... nothing. A quick 
investigation reveals the problem: the DVD is "region 1" and we live 
in "region 2". My anger rises, this is a legally bought DVD, inserted
into a legally bought DVD player connected to a legally bought
television. Why is my daughter not allowed to watch the film? The 
thought that my daughter has been denied this simple pleasure, not by
any fault but by *design* angers me even more and I resolve to do 
something about it.

I have a network enabled TV and I have a DLNA server so I decided 
to rip the movie and put it on the server. After all this is the only 
way my daughter is going to watch the film this Christmas.

But how to rip?

* A couple of years ago transcode was my weapon of choice but that is
  long since out of maintenance and the last time I tried it, it didn't
  work as it should.

* DVD::Rip is a front-end for transcode so no luck there either.

* I use Arista to transcode short movies taken from my (stills) camera 
  so I try this. It chokes, coming to a halt after the first pass.

* Acidrip is the closest I've found to a simple front end for mencoder 
  but it doesn't support x264 very well. I take a look for an up-to-date 
  version and discover that it too is out of maintenance.

So I give up looking and use mencoder from the command line. It's been 
years since I did this. It's fun but time-consuming wading through all
the options.

So I decide to write my own and base it on Acidrip.
