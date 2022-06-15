class Auth0Tag < Liquid::Tag
  def initialize(tag_name, params, tokens)
    super
    @target = params[1..].strip
  end

  def render(context)
    head_output = <<-HEREDOC
      <link rel="stylesheet" href="https://cdn.auth0.com/ulp/react-components/1.59.25/css/main.cdn.min.css">
      <style id="custom-styles-container">
        body {
          font-family: ulp-font, sans-serif;
        }
        :root {
          --primary-color: #ffa35c;
          --page-background-color: #ff0000;
        }
        .c15edc264 {
          background: transparent;
        }
        .no-js {
          clip: rect(0 0 0 0);
          clip-path: inset(50%);
          height: 1px;
          overflow: hidden;
          position: absolute;
          white-space: nowrap;
          width: 1px;
        }
      </style>
    HEREDOC
    widget_output = <<-HEREDOC
      <main class="_widget login">
      	<section class="_prompt-box-outer c082bfae4 ca9a51135">
      		<div class="ca7765aa4 cc0f204d0">
      			<div class="ce37485e0">
      				<header class="c88ace156 cbccf638c">
      					<div title="" id="custom-prompt-logo" style="background-color:transparent!important;background-position:50%!important;background-repeat:no-repeat!important;background-size:contain!important;height:60px!important;margin:auto!important;padding:0!important;position:static!important;width:auto!important"></div>
      					<img class="c804bd434 ca84a5be8" id="prompt-logo-center" src="https://cdn.auth0.com/styleguide/components/1.0.8/media/logos/img/badge.png" alt="">
      						<h1 class="c4faf1005 ce61d44fd">Welcome</h1>
      						<div class="c87ba88d2 cf51804e0">
      							<p class="c312fad3e cff44daea">Log in to  to continue to All Applications.</p>
      						</div>
      					</header>
      					<div class="c435f65a3 c5402e124">
      						<form method="post" class="cbc9e259c cc7ea13ef">
      							<input type="hidden" name="state" value="T-jbV6hF5ubZ8kk2uZcPVzr50qpAi486">
      								<div class="c3e5f2903 c421eb102">
      									<div class="c35e94f61">
      										<div class="_input-wrapper input-wrapper">
      											<div class="c290d0a77 c6502a50e c6ee2841c cc16b291d ce502c880 text" data-action-text="" data-alternate-action-text="">
      												<label class="c262a03d2 c44052fda ce8710345 no-js" for="username"> Email address </label>
      												<input class="c44d26365 c96d13227 focus input" inputmode="email" name="username" id="username" type="text" value="" required="" autocomplete="username" autocapitalize="none" spellcheck="false" autofocus="">
      													<div class="c262a03d2 c44052fda ce8710345 js-required" data-dynamic-label-for="username" aria-hidden="true"> Email address </div>
      												</div>
      											</div>
      											<div class="_input-wrapper input-wrapper">
      												<div class="c3ffd83c9 c6502a50e c6ee2841c ce502c880 password" data-action-text="" data-alternate-action-text="">
      													<label class="c262a03d2 c44052fda cc486081b no-js" for="password"> Password </label>
      													<input class="c1cea3c8c c96d13227 input" name="password" id="password" type="password" required="" autocomplete="current-password" autocapitalize="none" spellcheck="false">
      														<div class="c262a03d2 c44052fda cc486081b js-required" data-dynamic-label-for="password" aria-hidden="true"> Password </div>
      														<button type="button" class="_button-icon c14aa4d90 c7b79bfac ulp-button-icon" data-action="toggle">
      															<span aria-hidden="true" class="password-icon-tooltip show-password-tooltip">Show password</span>
      															<span aria-hidden="true" class="hide hide-password-tooltip password-icon-tooltip">Hide password</span>
      															<span class="password-toggle-label screen-reader-only" data-label="show-password">Show password</span>
      															<span class="hide password-toggle-label screen-reader-only" data-label="hide-password">Hide password</span>
      															<span class="c562b1cdd js-required password" aria-hidden="true"></span>
      														</button>
      													</div>
      												</div>
      											</div>
      										</div>
      										<p class="c70f3cc15 c9c35fad0">
      											<a class="c57d45e67 c7d975faf ce3b88cb1" href="/forgot-password">Forgot password?</a>
      										</p>
      										<div class="c83f0a9b3">
      											<button type="submit" name="action" value="default" class="c14aa4d90 c1eb66faa c75cd95bc c7b79bfac ccf4184c6">Continue</button>
      										</div>
      									</form>
      									<div class="__s16nu9 _alternate-action ulp-alternate-action">
      										<p class="c0bc001fe c312fad3e cff44daea">Don't have an account?#{' '}
      											<a class="c7d975faf ce3b88cb1" href="/signup">Sign up</a>
      										</p>
      									</div>
      								</div>
      							</div>
      						</div>
      					</section>
      				</main>
    HEREDOC
    case @target
    when "head"
      head_output
    when "widget"
      widget_output
    else
      raise "#{@target} is not supported. Try head or widget instead"
    end
  end
end
