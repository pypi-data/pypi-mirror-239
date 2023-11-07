from interactions import Extension, slash_command, SlashContext, Embed


class DynHelp(Extension):
    def __init__(self, bot, skip_coms: list = None, skip_opts: list = None):
        super().__init__()

        self.bot = bot
        self.skip_coms = skip_coms or []
        self.skip_opts = ["ctx"] + (skip_opts or [])

    @slash_command(
        name="help",
        description="Shows this message.",
    )
    async def help(self, ctx: SlashContext):
        try:
            # get a list of all the commands
            commands = ctx.bot.interaction_tree

            embed = Embed(
                title="Help",
                description="Here's a list of all the commands.",
            )

            print(f"Tree: {commands}")

            for _, tree in commands.items():
                for name, com in tree.items():
                    com = com.to_dict()
                    print(f"Command: {com}")

                    if name in self.skip_coms:
                        continue

                    name = com["name"]
                    description = com["description"].strip()
                    dm = com["dm_permission"]

                    print(f"Command: {name} - {description} - {dm}")

                    options = (
                        [
                            f"\n- `{name}`: {description} ({option['type']})" + (" DM allowed" if dm else "")
                            for option in com["options"]
                        ]
                        if "options" in com
                        else []
                    )

                    # parse options via docstring
                    if not options:
                        lines = description.split("\n")
                        new_line = []

                        for i, line in enumerate(lines):
                            print(f"Parsing line: {line}")
                            line = line.strip()

                            if line.startswith(":param"):
                                line = line.replace(":param", "").strip()
                                name, desc = line.split(":")

                                if name in self.skip_opts:
                                    continue

                                options.append(f"\n- `{name}`: {desc}")

                                print(f"Found option: {name} - {desc}")
                            elif ":return" in line:
                                ...
                            else:
                                new_line.append(line)

                        lines = new_line

                        description = "\n".join(lines)

                    embed.add_field(
                        name=f"`/{name}`",
                        value=f"{description.strip()}\n"
                              + (f"\nArgs:{'  '.join(options)}" if options else ""),
                        inline=True,
                    )
            await ctx.send(embed=embed, ephemeral=True, delete_after=60)
        except Exception as err:
            await ctx.send("An error occurred while running the command", ephemeral=True)
            raise err
