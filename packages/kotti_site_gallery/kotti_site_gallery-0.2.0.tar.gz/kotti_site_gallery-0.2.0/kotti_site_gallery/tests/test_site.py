class TestSiteImagesMethods:
    """
    Test methods which operate on the site's pictures.
    """
    def set_up(self):
        from kotti_site_gallery.resources import Site
        self.site = Site('www.frankfurt.de', title=u"Frankfurt",
                         body=u"<b>Foo! The bar.</b>")

        from kotti.resources import Image
        for name in ['foo', 'bar', 'cruz']:
            self.site[name] = Image(name=name, mimetype=u'image/jpeg')

        self.emty_site = Site('www.frankfurt.de', title=u"Frankfurt",
                              body=u"<b>Heyho.</b>")

    def test_get_icon(self, db_session):
        self.set_up()
        icon = self.site.get_icon()
        assert icon.name == 'foo'

        icon = self.emty_site.get_icon()
        assert icon is None

    def test_get_pictures(self, db_session):
        self.set_up()
        pictures = list(self.site.get_pictures())
        assert len(pictures) == 3
        assert pictures[2].name == 'cruz'

        pictures = list(self.emty_site.get_pictures())
        assert len(pictures) == 0
