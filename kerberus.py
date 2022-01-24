from commands import User, Tools


class Kerberus:
    users = list()

    def raz(self):
        t = Tools()
        t.browser.goto("http://localhost:6800/api/raz/hh4271")
        t.browser.close()

    def init_3players(self,size=3):
        self.raz()
        for i in range(size):
            u = User(i)
            self.users.append(u)

        i = 0
        for u in self.users:
            u.login("user" + str(i) + "@tester.com", "123456")
            if i == 0:
                if u.create_event(5):
                    u.publish_event(0)
            else:
                u.buy(0)
                u.close()

            i = i + 1

    def reconnexion_achat(self,size=2):
        for i in range(1, size + 1):
            u = User(i, "user" + str(i) + "@tester.com", "123456")
            u.buy(0)