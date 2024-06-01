import datetime

from sqlalchemy import DDL, DateTime, event, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class MixinTimeStamp(DeclarativeBase):
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    @classmethod
    def __create_func_for_update_at(cls) -> None:
        func_ddl = DDL(
            """DO $$
            BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_proc WHERE proname = 'refresh_updated_at') THEN
                CREATE FUNCTION public.refresh_updated_at()
                RETURNS TRIGGER
                LANGUAGE plpgsql NOT LEAKPROOF AS
                $BODY$
                    BEGIN
                       NEW.updated_at := now();
                        RETURN NEW;
                    END
                $BODY$;
            END IF;
        END;
        $$;
        """,
        )
        event.listen(cls.__table__, "before_create", func_ddl)

    @classmethod
    def __create_trigger_for_table(cls) -> None:
        trig_ddl = DDL(
            """CREATE TRIGGER tr_{}_updated_at BEFORE UPDATE
               ON {}
               FOR EACH ROW EXECUTE PROCEDURE
               refresh_updated_at();
            """.format(  # noqa P101
                cls.__tablename__,
                cls.__tablename__,
            ),
        )
        event.listen(cls.__table__, "after_create", trig_ddl)

    #
    @classmethod
    def __declare_last__(cls) -> None:
        cls.__create_func_for_update_at()
        cls.__create_trigger_for_table()
