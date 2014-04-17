jxnlco-django
=============

Collection of django apps I made for my website (jxnl.co)[http://jxnl.co]. 

## Blog

This the the model for a blog post on ym site. Instead of using traditional pagination, I've mapped my posts to a `Term` object so it relates my content to periods of my life instead of just meaningless numbers. Any post can be either `writing`, `project`, `art`, or `design` which is mainly to make my urls human readable url pattern and semantic. The urls only actually depends on the `pk` of the object. This is to say, while `jxnl.co/writing/2/title-of-post/` takes you to the second post I've written, `jxnl.co/asdasdasd/2/asdasdasdasd/` will point to the same post. All you really need to do is call `{{ entry.url }}` to get the semantic url. 

I actually developed this app, for the most part, with Test Driven Development. This was challenging and my first time really doing automated testing as part of my code.

## Resume

No tests, pretty messy. Having spent a month learning everything, I decided to try to make a modular resume app. Only took me 5 hours to start and design so I'm pretty pleased with that.

My goals for this app would be able to have tags for everything so I can generate different resumes for different specs. I would also like to create a view that generates a resume in .json. A whole resume templating system could come out of this if needed. However, LinkedIn probably does it pretty well.

If I need to or have time, I'll probably writes tests and improve the admin interface.
