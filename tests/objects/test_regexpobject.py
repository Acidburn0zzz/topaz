from ..base import BaseRuPyPyTest


class TestRegexpObject(BaseRuPyPyTest):
    def test_source(self, space):
        w_res = space.execute("return /abc/.source")
        assert space.str_w(w_res) == "abc"

    def test_compile_regexps(self, space):
        space.execute("""
        /^/
        /(a|b)/
        /(ab|ac)/
        /(ms|min)/
        /$/
        /[^f]/
        /[a]+/
        /\\(/
        /[()#:]/
        /[^()#:]/
        /([^)]+)?/
        /cy|m/
        /[\\-]/
        /(?!a)/
        /(?=a)/
        /a{1}/
        """)

    def test_match_operator(self, space):
        w_res = space.execute("""
        idx = /(l)(l)(o)(a)(b)(c)(h)(e)(l)/ =~ 'helloabchello'
        return idx, $1, $2, $3, $4, $5, $6, $7, $8, $9, $&, $+, $`, $'
        """)
        assert self.unwrap(space, w_res) == [2, "l", "l", "o", "a", "b", "c", "h", "e", "l", "lloabchel", "l", "he", "lo"]

    def test_new_regexp(self, space):
        w_res = space.execute("return Regexp.new('..abc..') == Regexp.compile('..abc..')")
        assert w_res is space.w_true

    def test_size(self, space):
        w_res = space.execute("""
        /(a)(b)(c)/ =~ "hey hey, abc, hey hey"
        return $~.size
        """)
        assert space.int_w(w_res) == 4

    def test_set_match_data_wrong_type(self, space):
        with self.raises(space, "TypeError"):
            space.execute("$~ = 12")
        space.execute("$~ = nil")