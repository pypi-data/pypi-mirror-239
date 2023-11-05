from datetime import datetime
from enum import IntEnum
from tortoise import fields
from tortoise_api_model import Model, TsModel, User as ApiUser, DatetimeSecField


class ClientStatus(IntEnum):
    me = 7
    my = 5
    own = 3
    pause = 2
    wait = 1
    block = 0


class AdvStatus(IntEnum):
    defActive = 0
    active = 1
    two = 2
    old = 3
    four = 4
    notFound = 9


class OrderStatus(IntEnum):
    zero = 0
    one = 1
    two = 2
    three = 3
    done = 4
    fifth = 5
    canceled = 6
    paid_and_canceled = 7
    # COMPLETED, PENDING, TRADING, BUYER_PAYED, DISTRIBUTING, COMPLETED, IN_APPEAL, CANCELLED, CANCELLED_BY_SYSTEM


class ExType(IntEnum):
    p2p = 1
    cex = 2
    main = 3  # p2p+cex
    dex = 4
    futures = 8


class DepType(IntEnum):
    earn = 1
    stake = 2
    beth = 3


class AssetType(IntEnum):
    spot = 1
    earn = 2
    found = 3


class Country(Model):
    id = fields.SmallIntField(pk=True)
    code: int = fields.IntField(null=True)
    short: str = fields.CharField(3, unique=True, null=True)
    name: str = fields.CharField(63, unique=True, null=True)
    cur: fields.ForeignKeyRelation["Cur"] = fields.ForeignKeyField("models.Cur", related_name="countries")
    curs: fields.ReverseRelation["Cur"]


class Cur(Model):
    id = fields.SmallIntField(pk=True)
    ticker: str = fields.CharField(3, unique=True)
    rate: float = fields.FloatField(null=True)
    blocked: bool = fields.BooleanField(default=False)
    country: str = fields.CharField(63, null=True)
    exs: fields.ManyToManyRelation["Ex"] = fields.ManyToManyField("models.Ex", through="curex", backward_key="curs")  # only root pts

    pts: fields.ManyToManyRelation["Pt"]
    ptcs: fields.ReverseRelation["Ptc"]
    pairs: fields.ReverseRelation["Pair"]
    countries: fields.ReverseRelation[Country]

    _name = 'ticker'
    class Meta:
        table_description = "Fiat currencies"


class Coin(Model):
    id: int = fields.SmallIntField(pk=True)
    ticker: str = fields.CharField(15, unique=True)
    rate: float = fields.FloatField(null=True)
    is_fiat: bool = fields.BooleanField(default=False)
    # quotable: bool = fields.BooleanField(default=False)
    exs: fields.ManyToManyRelation["Ex"] = fields.ManyToManyField("models.Ex", through="coinex", backward_key="coins")

    assets: fields.ReverseRelation["Asset"]
    deps: fields.ReverseRelation["Dep"]
    deps_reward: fields.ReverseRelation["Dep"]
    deps_bonus: fields.ReverseRelation["Dep"]

    async def repr(self):
        return f"{self.ticker}{self.is_fiat and ' (fiat)' or ''}"

    class Meta:
        table_description = "Crypro coins"


class Ex(Model):
    id: int = fields.SmallIntField(pk=True)
    name: str = fields.CharField(31)
    type: ExType = fields.IntEnumField(ExType)

    curs: fields.ManyToManyRelation[Cur] = [] # = fields.ManyToManyField("models.Cur", through="curex", backward_key="exs")
    coins: fields.ManyToManyRelation[Coin] = [] # = fields.ManyToManyField("models.Coin", through="coinex", backward_key="exs")
    pairs: fields.ReverseRelation["Pair"] = []
    deps: fields.ReverseRelation["Dep"] = []

    class Meta:
        table_description = "Exchanges"


class Pair(TsModel):
    id = fields.SmallIntField(pk=True)
    coin: fields.ForeignKeyRelation[Coin] = fields.ForeignKeyField("models.Coin", related_name="pairs")
    cur: fields.ForeignKeyRelation[Cur] = fields.ForeignKeyField("models.Cur", related_name="pairs")
    sell: bool = fields.BooleanField()
    fee: float = fields.FloatField()
    total: int = fields.IntField()
    ex: fields.ForeignKeyRelation[Ex] = fields.ForeignKeyField("models.Ex", related_name="pairs")
    ads: fields.ReverseRelation["Ad"]
    deps: fields.ReverseRelation["Dep"]

    class Meta:
        table_description = "Coin/Currency pairs"
        unique_together = (("coin", "cur", "sell", "ex"),)

    async def repr(self):
        return f"{self.coin.ticker}/{self.cur.ticker} {'SELL' if self.sell else 'BUY'}"


class User(ApiUser):
    client: fields.BackwardOneToOneRelation["Client"]
    agents: fields.BackwardFKRelation["Agent"]

class Client(TsModel):
    id: int = fields.SmallIntField(pk=True)
    name: str = fields.CharField(127)
    user: fields.OneToOneRelation[User] = fields.OneToOneField("models.User", related_name="client")
    user_id: int
    status: ClientStatus = fields.IntEnumField(ClientStatus, default=ClientStatus.wait)

    agents: fields.BackwardFKRelation["Agent"]

    _icon = 'heart-handshake'

    class Meta:
        table_description = "Our clients"

class Agent(TsModel):
    ex: fields.ForeignKeyRelation[Ex] = fields.ForeignKeyField("models.Ex", related_name="agents")
    auth: {} = fields.JSONField(null=True)
    client: fields.ForeignKeyRelation["Client"] = fields.ForeignKeyField("models.Client", related_name="agents")
    assets: fields.ReverseRelation["Asset"]
    orders: fields.ReverseRelation["Order"]
    ads: fields.ReverseRelation["Ad"]

    _icon = 'spy'

    async def repr(self):
        return (await self.client).name

    class Meta:
        table_description = "Agents"




class Adpt(Model):
    ad: fields.ForeignKeyRelation["Ad"] = fields.ForeignKeyField("models.Ad")
    pt: fields.ForeignKeyRelation["Pt"] = fields.ForeignKeyField("models.Pt")

    class Meta:
        table_description = "P2P Advertisements - Payment methods"

class Ad(Model):
    id: int = fields.BigIntField(pk=True)
    pair: fields.ForeignKeyRelation[Pair] = fields.ForeignKeyField("models.Pair")
    price: float = fields.FloatField()
    pts: fields.ManyToManyRelation["Pt"] = fields.ManyToManyField("models.Pt", through="adpt")  # only root pts
    maxFiat: float = fields.FloatField()
    minFiat: float = fields.FloatField()
    detail: str = fields.CharField(4095, null=True)
    autoMsg: str = fields.CharField(255, null=True)
    agent: fields.ForeignKeyRelation[Agent] = fields.ForeignKeyField("models.Agent", "ads")
    status: AdvStatus = fields.IntEnumField(AdvStatus)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True, index=True)

    orders: fields.ReverseRelation["Order"]

    _icon = 'ad'

    async def repr(self):
        return f"{(await self.pair).repr()}: {self.price:.3g}"

    class Meta:
        table_description = "P2P Advertisements"


class Pt(Model):
    name: str = fields.CharField(63)
    identifier: str = fields.CharField(63, unique=True, null=True)
    # todo: ex: many2many
    binance_id = fields.SmallIntField(unique=True, null=True)
    huobi_id = fields.SmallIntField(unique=True, null=True)
    template = fields.SmallIntField(null=True)  # default=0
    rank = fields.SmallIntField(default=0)
    type = fields.CharField(63, default='')
    group: str = fields.CharField(63, null=True)

    curs: fields.ManyToManyRelation[Cur] = fields.ManyToManyField("models.Cur", through="ptc")
    pairs: fields.ReverseRelation[Pair]
    orders: fields.ReverseRelation["Order"]
    children: fields.ReverseRelation["Pt"]
    ptcs: fields.ReverseRelation["Ptc"]

    _icon = 'currency'

    class Meta:
        table_description = "Payment methods"


class Ptc(Model):
    pt: fields.ForeignKeyRelation[Pt] = fields.ForeignKeyField("models.Pt")
    pt_id: int
    cur: fields.ForeignKeyRelation[Cur] = fields.ForeignKeyField("models.Cur")
    cur_id: int
    blocked: bool = fields.BooleanField(default=False)
    fiats: fields.ReverseRelation["Fiat"]

    _icon = 'currency'

    async def repr(self):
        return f"{(await self.pt).name}-{(await self.cur).ticker}"

    class Meta:
        table_description = "Payment methods - Currencies"
        unique_together = (("pt", "cur"),)


class Fiat(Model):
    ptc: fields.ForeignKeyRelation[Ptc] = fields.ForeignKeyField("models.Ptc")
    ptc_id: int
    # pts: fields.ManyToManyRelation[Pt] = fields.ManyToManyField("models.Pt", through="ptc") # no ptc.fiat_id field
    country: fields.ForeignKeyRelation[Country] = fields.ForeignKeyField("models.Country", related_name="fiats")
    country_id: int
    detail: str = fields.CharField(127)
    agent: fields.ForeignKeyRelation[Agent] = fields.ForeignKeyField("models.Agent", "fiats")
    agent_id: int
    amount: float = fields.FloatField(default=None, null=True)
    target: float = fields.FloatField(default=None, null=True)

    orders: fields.ReverseRelation["Order"]

    _icon = 'cash'

    async def repr(self):
        return f"{self.id}: {(await self.ptc).repr()} ({(await self.agent).repr()})"

    class Meta:
        table_description = "Currency accounts balance"


class Route(Model):
    ptc_from: fields.ForeignKeyRelation[Ptc] = fields.ForeignKeyField("models.Ptc", related_name="out_routes")
    ptc_to: fields.ForeignKeyRelation[Ptc] = fields.ForeignKeyField("models.Ptc", related_name="in_routes")


class Limit(Model):
    route: fields.ForeignKeyRelation[Route] = fields.ForeignKeyField("models.Route")
    limit: int = fields.IntField(default=-1, null=True)  # '$' if unit >= 0 else 'transactions count'
    unit: int = fields.IntField(default=30)  # positive: $/days, 0: $/transaction, negative: transactions count / days
    fee: float = fields.IntField(default=0, null=True)  # on multiply Limits for one Route - fees is quanting by minimum unit if units equal, else summing


class Asset(Model):
    coin: fields.ForeignKeyRelation[Coin] = fields.ForeignKeyField("models.Coin", related_name="assets")
    coin_id: int
    agent: fields.ForeignKeyRelation[Agent] = fields.ForeignKeyField("models.Agent", "assets")
    agent_id: int
    ex: fields.ForeignKeyRelation[Ex] = fields.ForeignKeyField("models.Ex", "assets")
    ex_id: int
    type: AssetType = fields.IntEnumField(AssetType)
    free: float = fields.FloatField()
    freeze: float|None = fields.FloatField(default=0)
    lock: float|None = fields.FloatField(default=0)
    target: float = fields.FloatField(default=0, null=True)

    _icon = 'bitcoin'

    async def repr(self):
        return f'{self.coin_id} {self.free:.3g}/{self.freeze:.3g} user:{(await self.agent).repr()}'

    class Meta:
        table_description = "Coin balance"
        unique_together = (("coin", "agent", "ex", "type"),)


class Order(TsModel):
    id: int = fields.BigIntField(pk=True)
    ad: fields.ForeignKeyRelation[Ad] = fields.ForeignKeyField("models.Ad", related_name="ads")
    ad_id: int
    amount: float = fields.FloatField()
    fiat: fields.ForeignKeyRelation[Fiat] = fields.ForeignKeyField("models.Fiat", related_name="orders", null=True)
    fiat_id: int
    pt: fields.ForeignKeyRelation[Pt] = fields.ForeignKeyField("models.Pt", related_name="orders", null=True)
    pt_id: int
    taker: fields.ForeignKeyRelation[Agent] = fields.ForeignKeyField("models.Agent", "orders")
    taker_id: int
    status: OrderStatus = fields.IntEnumField(OrderStatus)
    notify_pay_at: datetime = DatetimeSecField(null=True)
    confirm_pay_at: datetime = DatetimeSecField(null=True)

    _icon = 'invoice'

    async def repr(self):
        return f'{self.amount:.3g} pt:{(await self.pt).name}/{self.fiat_id} {self.status.name}'

    class Meta:
        table_description = "P2P Orders"

class Dep(TsModel):
    pid: str = fields.CharField(31)  # product_id
    apr: float = fields.FloatField()
    fee: float = fields.FloatField(null=True)
    apr_is_fixed: bool = fields.BooleanField(default=False)
    duration: int = fields.SmallIntField(null=True)
    early_redeem: bool = fields.BooleanField(null=True)
    type: DepType = fields.IntEnumField(DepType)
    # mb: renewable?
    min_limit: float = fields.FloatField()
    max_limit: float = fields.FloatField(null=True)
    is_active: bool = fields.BooleanField(default=True)

    coin: fields.ForeignKeyRelation[Coin] = fields.ForeignKeyField("models.Coin", related_name="deps")
    coin_id: int
    reward_coin: fields.ForeignKeyRelation[Coin] = fields.ForeignKeyField("models.Coin", related_name="deps_reward", null=True)
    reward_coin_id: int = None
    bonus_coin: fields.ForeignKeyRelation[Coin] = fields.ForeignKeyField("models.Coin", related_name="deps_bonus", null=True)
    bonus_coin_id: int = None
    ex: fields.ForeignKeyRelation[Ex] = fields.ForeignKeyField("models.Ex", related_name="deps")
    ex_id: int
    investments: fields.ReverseRelation["Investment"]

    _icon = 'grow'

    async def repr(self):
        return f'{self.apr*100:.3g}% {f"{self.duration}d" if self.duration and self.duration>0 else "flex"}'

    class Meta:
        table_description = "Investment products"
        unique_together = (("pid", "type", "ex"),)

class Investment(TsModel):
    dep: fields.ForeignKeyRelation[Dep] = fields.ForeignKeyField("models.Dep", related_name="investments")
    dep_id: int
    amount: float = fields.FloatField()
    is_active: bool = fields.BooleanField(default=True)

    _icon = 'grow'

    async def repr(self):
        return f'{self.amount:.3g} {(await self.dep).repr()}'

    class Meta:
        table_description = "Investments"
